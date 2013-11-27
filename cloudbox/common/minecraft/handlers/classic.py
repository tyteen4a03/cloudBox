# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import hashlib

from twisted.internet.task import LoopingCall
from zope.interface import implements

from cloudbox.common.constants.common import *
from cloudbox.common.constants.classic import *
from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.interfaces import IMinecraftPacketHandler
from cloudbox.common.util import packString


class BaseMinecraftPacketHandler(BasePacketHandler):
    """
    Base packet handler for all Minecraft packets.
    """
    implements(IMinecraftPacketHandler)

    @classmethod
    def unpackData(cls, data):
        return TYPE_FORMATS[cls.packetID].decode(data)

    @classmethod
    def getExpectedLength(cls):
        return len(TYPE_FORMATS[cls.packetID])


class HandshakePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Login requests.
    """
    packetID = TYPE_INITIAL

    @classmethod
    def handleData(cls, data):
        # Get the client's details
        protocol, data["parent"].username, mppass, utype = data["packetData"]
        if data["parent"].identified:
            # Sent two login packets - I wonder why?
            data["parent"].factory.logger.info("Kicked '%s'; already logged in to server" % data["parent"].username)
            data["parent"].sendError("You already logged in!")

        # Right protocol?
        if protocol != 7:
            data["parent"].sendError("Wrong protocol.")
            return

        # Check their password
        expectedPassword = hashlib.md5(data["parent"].factory.settings["main"]["salt"] +
                                       data["parent"].username).hexdigest()[-32:].strip("0")
        mppass = mppass.strip("0")
        # TODO: Rework this - possibly limit to localhost only?
        #if not data["parent"].transport.getHost().host.split(".")[0:2] == data["parent"].ip.split(".")[0:2]:
        if mppass != expectedPassword:
            data["parent"].factory.logger.info(
                "Kicked '%s'; invalid password (%s, %s)" % (data["parent"].username, mppass, expectedPassword))
            data["parent"].sendError("Incorrect authentication, please try again.")
            return
        #value = data["parent"].factory.runHook("prePlayerConnect", {"client": self})

        # Are they banned?
        bans = data["parent"].factory.getBans(data["parent"].username, data["parent"].ip)
        if bans:
            data["parent"].sendError("You are banned: %s" % bans[-1]["reason"])
            return

        # OK, see if there's anyone else with that username
        usernameList = data["parent"].factory.buildUsernameList()
        if data["parent"].username.lower() in usernameList:
            # Kick the other guy out
            data["parent"].factory.clients[usernameList[data["parent"].username.lower()].id]["protocol"].sendError(
                "You logged in on another computer.", disconnectNow=True)
            return

        # All check complete. Request World Server to prepare level
        data["parent"].identified = True
        data["parent"].factory.clients[data["parent"].id]["username"] = data["parent"].username
        data["parent"].factory.joinDefaultWorld(data["parent"])

        # Announce our presence
        data["parent"].factory.logger.info("Connected, as '%s'" % data["parent"].username)
        #for client in data["parent"].factory.usernames.values():
        #    client.sendServerMessage("%s has come online." % data["parent"].username)

        # Send them back our info.
        # TODO: CPE
        #if data["parent"].factory.settings["main"]["enable-cpe"]:
        #    data["parent"].sendPacket(TYPE_EXTINFO, len(data["parent"].cpeExtensions)

        data["parent"].sendPacket(TYPE_INITIAL, {
            "protocolVersion": 7, # Protocol version
            "serverName": packString(data["parent"].factory.settings["main"]["name"]),
            "serverMOTD": packString(data["parent"].factory.settings["main"]["motd"]),
            #"userPermission": 100 if (self.isOp() if hasattr(self, "world") else False) else 0, # TODO
            "userPermission": 0
        })
        data["parent"].loops.registerLoop("keepAlive", LoopingCall(data["parent"].sendKeepAlive)).start(1)
        #data["parent"].factory.runHook("onPlayerConnect", {"client": data["parent"]}) # Run the player connect hook

    @classmethod
    def packData(cls, data):
        return TYPE_FORMATS[TYPE_INITIAL].encode(data["protocolVersion"],
                                                 data["serverName"],
                                                 data["serverMOTD"],
                                                 data["userPermission"])


class KeepAlivePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Keep Alives.
    """
    packetID = TYPE_KEEPALIVE

    @classmethod
    def packData(cls, data):
        return ""


class LevelInitPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Initialization.
    """
    packetID = TYPE_LEVELINIT

    @classmethod
    def packData(cls, data):
        pass


class LevelDataPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Chunks.
    """
    packetID = TYPE_LEVELDATA

    @classmethod
    def packData(cls, data):
        pass


class LevelFinalizePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Level Finalization.
    """
    packetID = TYPE_LEVELFINALIZE

    @classmethod
    def packData(cls, data):
        pass


class BlockChangePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Block Changes.
    """
    packetID = TYPE_BLOCKCHANGE

    @classmethod
    def handleData(cls, data):
        if data["serverType"] == SERVER_TYPES["WorldServer"]:
            x, y, z, created, block = data["packetData"]
            if not data["parent"].identified:
                data["parent"].factory.logger.info(
                    "Kicked '%s'; did not send a login before building" % data["parent"].ip)
                data["parent"].sendError("Provide an authentication before building.")
                return
            if block == 255:
                # Who sends 255 anyway?
                data["parent"].factory.logger.debug("%s sent block 255 as 0" % data["parent"].username)
                block = 0
            # Check if out of block range or placing invalid blocks
            if block not in BLOCKS.keys() or block in [BLOCKS_BY_NAME["water"], BLOCKS_BY_NAME["lava"]]:
                data["parent"].factory.logger.info("Kicked '%s' (IP %s); Tried to place invalid block %s" % (
                                        data["parent"].username, data["parent"].ip, block))
                data["parent"].sendError("Invalid blocks are not allowed!")
                return
            # TODO Permission Manager
            if block == 7:  # and not permissionManager.hasWorldPermission(data["parent"].permissions):
                data["parent"].factory.logger.info("Kicked '%s'; Tried to place bedrock." % data["parent"].ip)
                data["parent"].sendError("Don't build bedrocks!")
                return
            try:
            # If we're read-only, reverse the change
                allowBuilding = data["parent"].factory.runHook(
                    "onBlockClick",
                    {"x": x, "y": y, "z": z, "block": block, "client": data["parent"]}
                )
                if not allowBuilding:
                    data["parent"].sendBlock(x, y, z)
                    return
                # Track if we need to send back the block change
                overridden = False
                selectedBlock = block
                # If we're deleting, block is actually air
                # (note the selected block is still stored as selectedBlock)
                if not created:
                    block = 0
                # Pre-hook, for stuff like /paint
                new_block = data["parent"].factory.runHook("preBlockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": data["parent"]})
                if new_block is not None:
                    block = new_block
                    overridden = True
                # Block detection hook that does not accept any parameters
                data["parent"].factory.runHook(
                    "blockDetect",
                    {"x": x, "y": y, "z": z, "block": block, "client": data["parent"]}
                )
                # Call hooks
                new_block = data["parent"].factory.runHook(
                    "blockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": data["parent"]}
                )
                if new_block is False:
                    # They weren't allowed to build here!
                    data["parent"].sendBlock(x, y, z)
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
                data["parent"].world[x, y, z] = chr(block)
                # Now, send the custom block back if we need to
                if overridden:
                    data["parent"].sendBlock(x, y, z, block)
            # Out of bounds!
            except (KeyError, AssertionError):
                data["parent"].sendPacket(TYPE_BLOCKSET, x, y, z, "\0")
            # OK, replay changes to others
            else:
                data["packetData"].factory.queue.put((data["parent"], TASK_BLOCKSET, (x, y, z, block)))
        else:
            # Hand it over to the WorldServer
            data["parent"].factory.relayMCPacketToWorldServer(TYPE_BLOCKCHANGE, data["packetData"])


class BlockSetPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for Setting a Block.
    """
    packetID = TYPE_BLOCKSET

    @classmethod
    def packData(cls, data):
        pass


class SpawnPlayerPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player spawning.
    """
    packetID = TYPE_SPAWNPLAYER

    @classmethod
    def packData(cls, data):
        pass


class PlayerPosPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player position updates.
    """
    packetID = TYPE_PLAYERPOS

    @classmethod
    def handleData(cls, data):
        pass

    @classmethod
    def packData(cls, data):
        pass


class PlayerOrtPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player orientation updates.
    """
    packetID = TYPE_PLAYERORT

    @classmethod
    def packData(cls, data):
        pass


class PlayerDespawnPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for player despawning.
    """
    packetID = TYPE_PLAYERDESPAWN

    @classmethod
    def packData(cls, data):
        return TYPE_FORMATS[cls.packetID].encode(data["playerID"])


class MessagePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for messages.
    """
    packetID = TYPE_MESSAGE

    @classmethod
    def handleData(cls, data):
        pass

    @classmethod
    def packData(cls, data):
        pass


class ErrorPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for error messages.
    """
    packetID = TYPE_ERROR

    @classmethod
    def packData(cls, data):
        return TYPE_FORMATS[cls.packetID].encode(data["error"])


class SetUserTypePacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler for setting op permissions.
    """
    packetID = TYPE_SETUSERTYPE

    @classmethod
    def packData(cls, data):
        pass