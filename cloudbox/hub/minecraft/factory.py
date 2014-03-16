# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from netaddr import IPAddress
from twisted.internet import defer
from twisted.internet.protocol import ServerFactory
from twisted.internet.defer import Deferred, DeferredList
from twisted.python.failure import Failure

from cloudbox.common.constants.classic import *
from cloudbox.common.constants.common import *
from cloudbox.common.constants.cpe import *
from cloudbox.common.database import checkForFailure
from cloudbox.common.exceptions import ErrorCodeException
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxFactoryMixin, TaskTickMixin
from cloudbox.common.models.servers import WorldServer
from cloudbox.common.models.user import Bans, User, UserIP
from cloudbox.common.models.world import World
from cloudbox.hub.exceptions import WorldServerLinkException
from cloudbox.hub.minecraft.protocol import MinecraftHubServerProtocol


class MinecraftHubServerFactory(ServerFactory, CloudBoxFactoryMixin, TaskTickMixin):
    """
    I am the Minecraft side of the hub. I handle Minecraft client requests and pass them on to World Servers.
    """
    protocol = MinecraftHubServerProtocol

    IS_CLIENT = False

    def __init__(self, parentService):
        self.parentService = parentService
        self.clients = {}
        self.logger = logging.getLogger("cloudbox.hub.mc.factory")
        self.loops = LoopRegistry()
        self.loops.registerLoop("task", self.taskLoop).start(self.getTickInterval())

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def buildHandlers(self):
        handlers = {
            TYPE_INITIAL: ("cloudbox.common.minecraft.handlers.classic", "HandshakePacketHandler"),
            TYPE_KEEPALIVE: ("cloudbox.common.minecraft.handlers.classic", "KeepAlivePacketHandler"),
            TYPE_LEVELINIT: ("cloudbox.common.minecraft.handlers.classic", "LevelInitPacketHandler"),
            TYPE_LEVELDATA: ("cloudbox.common.minecraft.handlers.classic", "LevelDataPacketHandler"),
            TYPE_LEVELFINALIZE: ("cloudbox.common.minecraft.handlers.classic", "LevelFinalizePacketHandler"),
            TYPE_BLOCKCHANGE: ("cloudbox.common.minecraft.handlers.classic", "BlockChangePacketHandler"),
            TYPE_BLOCKSET: ("cloudbox.common.minecraft.handlers.classic", "BlockSetPacketHandler"),
            TYPE_SPAWNPLAYER: ("cloudbox.common.minecraft.handlers.classic", "SpawnPlayerPacketHandler"),
            TYPE_PLAYERPOS: ("cloudbox.common.minecraft.handlers.classic", "PlayerPosPacketHandler"),
            TYPE_PLAYERORT: ("cloudbox.common.minecraft.handlers.classic", "PlayerOrtPacketHandler"),
            TYPE_PLAYERDESPAWN: ("cloudbox.common.minecraft.handlers.classic", "PlayerDespawnPacketHandler"),
            TYPE_MESSAGE: ("cloudbox.common.minecraft.handlers.classic", "MessagePacketHandler"),
            TYPE_ERROR: ("cloudbox.common.minecraft.handlers.classic", "ErrorPacketHandler"),
            TYPE_SETUSERTYPE: ("cloudbox.common.minecraft.handlers.classic", "SetUserTypePacketHandler")
        }
        if self.settings["main"]["enable-cpe"]:
            handlers.update({
                TYPE_EXTINFO: ("cloudbox.common.minecraft.handlers.cpe", "ExtInfoPacketHandler"),
                TYPE_EXTENTRY: ("cloudbox.common.minecraft.handlers.cpe", "ExtInfoPacketHandler")
            })
        return handlers

    def claimID(self, proto):
        """
        Fetches ID for a client protocol instance.
        """
        for i in range(1, self.settings["main"]["max-clients"] + 1):
            if i not in self.clients:
                self.clients[i] = {"username": None, "protocol": proto}
                # TODO - Hook Call Here
                return i
        # Server is full
        return None

    def releaseID(self, clientID):
        del self.clients[clientID]

    ### World Server related functions ###

    def getWorldServersAvailability(self):
        statDict = {}
        for ws in self.getFactory("WorldServerCommServerFactory").worldServers:
            statDict[ws.id] = self.getWorldServerAvailability(ws.id)

    def getWorldServerAvailability(self, wsID):
        return self.getFactory("WorldServerCommServerFactory").worldServers[wsID].getStats()

    def relayMCPacketToWorldServer(self, packetID, packetData):
        pass

    def assignWorldServer(self, proto, world=None):
        if not world:
            world = "default"  # TODO Link to settings
        assert proto.worldServer is None, "Tried to reassign already assigned client."

        def afterAddedNewClient(wsProto):
            # Confirm the assginment
            proto.worldServer = wsProto

        def gotWorldServer(res):
            checkForFailure(res)
            if not res:
                raise ErrorCodeException(ERRORS["no_results"])
            ws = res[0]["worldServerID"]
            if ws not in self.getFactory("WorldServerCommServerFactory").worldServers:
                raise WorldServerLinkException(ERRORS["worldserver_link_not_established"])
            wsProto = self.getFactory("WorldServerCommServerFactory").worldServers[ws]
            return wsProto.protoDoJoinServer(proto, world).addCallback(afterAddedNewClient, wsProto)

        return self.db.runQuery(World.select(World.worldServerID).where(World.name == world).sql()).addBoth(gotWorldServer)

    def buildUsernameList(self, wsID=None):
        """
        Builds a list of {username: client object} by the client list, or
        specify a WorldServer ID to filter.
        """
        theList = dict()
        for cID, cEntry in self.clients.items():
            if cEntry["username"]:
                if wsID:
                    if cEntry["proto"].wsID == wsID:
                        theList[cEntry["username"].lower()] = cEntry["protocol"]
                else:
                    theList[cEntry["username"].lower()] = cEntry["protocol"]
        return theList

    def getBans(self, username=None, ip=None):
        """
        Fetches the ban information using the information given - username, IP, or both.
        @param username The username to query for.
        @param ip The IP to query for.
        @return Deferred The deferred object.
        """
        assert not (username is None and ip is None)

        def afterGetUser(res):
            checkForFailure(res)
            if not res:  # First time user
                return []
            return self.db.runQuery(Bans.select().where(Bans.type == BAN_TYPES["globalBan"] & Bans.username == res[0]["username"]).sql()).addBoth(afterGetBans, username)

        def afterGetIP(res):
            checkForFailure(res)
            if not res:  # First time visitor
                return []
            return self.db.runQuery(Bans.select().where(Bans.type == BAN_TYPES["globalIPBan"] & Bans.recordID == res[0]["id"])).addBoth(afterGetBans, str(ip))

        def afterGetBans(res, lookupEntity):
            checkForFailure(res)
            if not res:
                return []
            elif len(res) > 1:
                # More than one record...
                self.logger.warn("Multiple global ban detected for lookup entity {}.", lookupEntity)
            return res[0]

        if username and ip is None:
            # We need the user id first
            return self.db.runQuery(User.select(User.id).where(User.username == username).sql()).addBoth(afterGetUser)
        elif ip and username is None:
            # We need the IP id first
            if not isinstance(ip, IPAddress):
                ip = IPAddress(ip)

            return self.db.runQuery(UserIP.select(UserIP.id).where(UserIP.ip == int(ip))).addBoth(afterGetIP)
        # TODO
        #elif ip and username:

    def getUser(self, username=None, userID=None):
        """
        Fetches the user record for database population. Specify either username or userID, not both!
        @param username The username to query for.
        @param userID The userID to query for.
        @return tuple The user record.
        """
        assert not (username is None and userID is None)
        assert not (username and userID)


    ### Handler methods ###
