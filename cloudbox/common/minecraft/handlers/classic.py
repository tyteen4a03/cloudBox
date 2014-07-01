# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import hashlib
import time

from twisted.internet.defer import Deferred
from twisted.internet.task import LoopingCall
from zope.interface import implements

from cloudbox.common.constants.common import *
from cloudbox.common.constants.classic import *
from cloudbox.common.database import hasFailed
from cloudbox.common.exceptions import DatabaseServerLinkException
from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.interfaces import IMinecraftPacketHandler
from cloudbox.common.models.user import User, UserServiceAssoc
from cloudbox.common.util import packString


class BaseMinecraftPacketHandler(BasePacketHandler):
    """
    Base packet handler for all Minecraft packets.
    """
    implements(IMinecraftPacketHandler)

    def unpackData(self, data):
        return TYPE_FORMATS[self.packetID].decode(data)

    @property
    def expectedLength(self):
        return len(TYPE_FORMATS[self.packetID])


class HandshakePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Login requests.
    """
    packetID = TYPE_INITIAL

    def handleData(self, packetData, requestID=None):
        # Get the client's details
        protocol, self.parent.player["username"], mppass, utype = packetData
        if self.parent.identified:
            # Sent two login packets - I wonder why?
            self.parent.factory.logger.info("Kicked '%s'; already logged in to server" % self.parent.player["username"])
            self.parent.sendError("You already logged in!")

        # Right protocol?
        if protocol != 7:
            self.parent.sendError("Wrong protocol.")
            return

        # Check their password
        expectedPassword = hashlib.md5(self.parent.factory.settings["main"]["salt"] +
                                       self.parent.player["username"]).hexdigest()[-32:].strip("0")
        mppass = mppass.strip("0")
        # TODO: Rework this - possibly limit to localhost only?
        #if not self.parent.transport.getHost().host.split(".")[0:2] == self.parent.ip.split(".")[0:2]:
        if mppass != expectedPassword:
            self.parent.factory.logger.info(
                "Kicked '%s'; invalid password (%s, %s)" % (self.parent.player["username"], mppass, expectedPassword))
            self.parent.sendError("Incorrect authentication, please try again.")
            return
        #value = self.parent.factory.runHook("prePlayerConnect", {"client": self})

        def populateData(res):
            failed = hasFailed(res)

            def actuallyPopulateData(theRes):
                if hasFailed(theRes):
                    self.parent.sendError("The server is currently not available. Please try again later.")
                    raise DatabaseServerLinkException(ERRORS["data_corrupt"])
                for key, value in u:
                    self.parent.player["key"] = value

            if not res:
                # User not found, populate with default variables
                u = User.create(
                    id=uuid.uuid5(UUID["cloudbox.users"], self.parent.player["username"]),
                    username=self.parent.player["username"],
                    firstseen=time.time(),
                    lastseen=time.time(),
                )

                def step2(theRes):
                    if hasFailed(theRes):
                        self.parent.sendError("The server is currently not available. Please try again later.")
                        raise DatabaseServerLinkException(ERRORS["data_corrupt"])
                    self.parent.db.runQuery(*UserServiceAssoc.create(
                        id=theRes,
                        service=1,  # Right now force ClassiCube
                        verified=1,  # Of course we're verified
                    ).sql()).addCallback(actuallyPopulateData)

                self.parent.db.runQuery(*u.sql()).addBoth(step2)
            else:
                # User found. Populate
                self.parent.db.runQuery(*User.select().where(User.id == res).sql()).addBoth(actuallyPopulateData)

        def afterAssignedWorldServer(res):
            self.logger.info(res)
            self.parent.joinDefaultWorld()
            # Announce our presence
            self.parent.factory.logger.info("Connected, as '%s'" % self.parent.player["username"])
            #for client in self.parent.factory.usernames.values():
            #    client.sendServerMessage("%s has come online." % self.parent.player["username"])

            # Send them back our info.
            # TODO: CPE
            #if self.parent.factory.settings["main"]["enable-cpe"]:
            #    self.parent.sendPacket(TYPE_EXTINFO, len(self.parent.cpeExtensions)

            self.parent.sendPacket(TYPE_INITIAL, {
                "protocolVersion": 7,  # Protocol version
                "serverName": packString(self.parent.factory.settings["main"]["name"]),
                "serverMOTD": packString(self.parent.factory.settings["main"]["motd"]),
                #"userPermission": 100 if (self.isOp() if hasattr(self, "world") else False) else 0, # TODO
                "userPermission": 0
            })
            self.parent.loops.registerLoop("keepAlive", LoopingCall(self.parent.sendKeepAlive)).start(1)

        def gotData(results):
            # OK, see if there's anyone else with that username
            usernameList = self.parent.factory.buildUsernameList()
            if self.parent.player["username"].lower() in usernameList:
                # Kick the other guy out
                self.parent.factory.clients[usernameList[self.parent.player["username"]]]["protocol"].sendError(
                    "You logged in on another computer.", disconnectNow=True)
                return

            # All check complete. Request World Server to prepare level
            self.parent.identified = True
            self.parent.factory.assignWorldServer(self.parent).addBoth(afterAssignedWorldServer)

        def gotBans(data):
            # Are they banned?
            if data:
                self.parent.sendError("You are banned: {}".format(data["reason"]))
                return
            self.parent.factory.getUserByUsername(self.parent.player["username"]).addBoth(populateData).addBoth(gotData)

        returned = self.parent.factory.getBans(self.parent.player["username"])
        if isinstance(returned, Deferred):
            returned.addBoth(gotBans)
        else:
            gotBans(returned)

    def packData(self, packetData):
        return TYPE_FORMATS[TYPE_INITIAL].encode(packetData["protocolVersion"],
                                                 packetData["serverName"],
                                                 packetData["serverMOTD"],
                                                 packetData["userPermission"])


class KeepAlivePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Keep Alives.
    """
    packetID = TYPE_KEEPALIVE

    def packData(self, packetData):
        return ""


class LevelInitPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Initialization.
    """
    packetID = TYPE_LEVELINIT

    def packData(self, packetData):
        pass


class LevelDataPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Chunks.
    """
    packetID = TYPE_LEVELDATA

    def packData(self, packetData):
        pass


class LevelFinalizePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Finalization.
    """
    packetID = TYPE_LEVELFINALIZE

    def packData(self, packetData):
        pass


class BlockChangePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Block Changes.
    """
    packetID = TYPE_BLOCKCHANGE

    def handleData(self, packetData, requestID=None):
        if self.parent.serverType == SERVER_TYPES["WorldServer"]:
            x, y, z, created, block = packetData
            if not self.parent.identified:
                self.parent.factory.logger.info(
                    "Kicked '%s'; did not send a login before building" % self.parent.ip)
                self.parent.sendError("Provide an authentication before building.")
                return
            if block == 255:
                # Who sends 255 anyway?
                self.parent.factory.logger.debug("%s sent block 255 as 0" % self.parent.player["username"])
                block = 0
            # Check if out of block range or placing invalid blocks
            if block not in BLOCKS.keys() or block in [BLOCKS_BY_NAME["water"], BLOCKS_BY_NAME["lava"]]:
                self.parent.factory.logger.info("Kicked '%s' (IP %s); Tried to place invalid block %s" % (
                                        self.parent.player["username"], self.parent.ip, block))
                self.parent.sendError("Invalid blocks are not allowed!")
                return
            # TODO Permission Manager
            if block == 7:  # and not permissionManager.hasWorldPermission(self.parent.permissions):
                self.parent.factory.logger.info("Kicked '%s'; Tried to place bedrock." % self.parent.ip)
                self.parent.sendError("Don't build bedrocks!")
                return
            try:
            # If we're read-only, reverse the change
                allowBuilding = self.parent.factory.runHook(
                    "onBlockClick",
                    {"x": x, "y": y, "z": z, "block": block, "client": self.parent}
                )
                if not allowBuilding:
                    self.parent.sendBlock(x, y, z)
                    return
                # Track if we need to send back the block change
                overridden = False
                selectedBlock = block
                # If we're deleting, block is actually air
                # (note the selected block is still stored as selectedBlock)
                if not created:
                    block = 0
                # Pre-hook, for stuff like /paint
                new_block = self.parent.factory.runHook("preBlockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": self.parent})
                if new_block is not None:
                    block = new_block
                    overridden = True
                # Block detection hook that does not accept any parameters
                self.parent.factory.runHook(
                    "blockDetect",
                    {"x": x, "y": y, "z": z, "block": block, "client": self.parent}
                )
                # Call hooks
                new_block = self.parent.factory.runHook(
                    "blockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": self.parent}
                )
                if new_block is False:
                    # They weren't allowed to build here!
                    self.parent.sendBlock(x, y, z)
                    return
                # TODO Use object as hint
                elif new_block == -1:
                    # Someone else handled building, just continue
                    return
                elif new_block is not None:
                    if not new_block:
                        block = new_block
                        overridden = True
                # OK, save the block
                self.parent.world[x, y, z] = chr(block)
                # Now, send the custom block back if we need to
                if overridden:
                    self.parent.sendBlock(x, y, z, block)
            # Out of bounds!
            except (KeyError, AssertionError):
                self.parent.sendPacket(TYPE_BLOCKSET, x, y)
            # OK, replay changes to others
            else:
                self.parent.factory.queue.put((self.parent, TASK_BLOCKSET, (x, y, z, block)))
        else:
            # Hand it over to the WorldServer
            self.parent.factory.relayMCPacketToWorldServer(TYPE_BLOCKCHANGE,packetData)


class BlockSetPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Setting a Block.
    """
    packetID = TYPE_BLOCKSET

    def packData(self, packetData):
        pass


class SpawnPlayerPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player spawning.
    """
    packetID = TYPE_SPAWNPLAYER

    def packData(self, packetData):
        pass


class PlayerPosPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player position updates.
    """
    packetID = TYPE_PLAYERPOS

    def handleData(self, packetData, requestID=None):
        pass

    def packData(self, packetData):
        pass


class PlayerOrtPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player orientation updates.
    """
    packetID = TYPE_PLAYERORT

    def packData(self, packetData):
        pass


class PlayerDespawnPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player despawning.
    """
    packetID = TYPE_PLAYERDESPAWN

    def packData(self, packetData):
        return TYPE_FORMATS[self.packetID].encode(packetData["playerID"])


class MessagePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for messages.
    """
    packetID = TYPE_MESSAGE

    def handleData(self, packetData, requestID=None):
        pass

    def packData(self, packetData):
        pass


class ErrorPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for error messages.
    """
    packetID = TYPE_ERROR

    def packData(self, packetData):
        self.logger.info("Sending error to client: {}".format(packetData["error"]))
        return TYPE_FORMATS[self.packetID].encode(packetData["error"])


class SetUserTypePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler for setting op permissions.
    """
    packetID = TYPE_SETUSERTYPE

    def packData(self, packetData):
        pass