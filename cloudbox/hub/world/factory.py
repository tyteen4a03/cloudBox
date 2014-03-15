# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from twisted.internet.defer import Deferred, DeferredList
from twisted.internet.protocol import ServerFactory

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxFactoryMixin, TaskTickMixin
from cloudbox.hub.world.protocol import WorldServerCommServerProtocol


class WorldServerCommServerFactory(ServerFactory, CloudBoxFactoryMixin, TaskTickMixin):
    """
    I listen to World Servers and interact with them, acting as a proxy.
    """

    protocol = WorldServerCommServerProtocol
    remoteServerType = SERVER_TYPES["WorldServer"]

    IS_CLIENT = False

    def __init__(self, parentService):
        self.parentService = parentService
        self.worldServers = {}
        self.logger = logging.getLogger("cloudbox.hub.world.factory")
        self.loops = LoopRegistry()
        self.loops.registerLoop("tasks", self.taskLoop)

    def startFactory(self):
        self.handlers = self.buildHandlers()
        self.loops["tasks"].start(self.getTickInterval())

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_WORLD_SERVER.items())
        h[TYPE_HANDSHAKE] = ("cloudbox.hub.handlers", "HubHandshakePacketHandler")
        return h

    def getServerStats(self):
        """
        Gets the current load for each World Server.
        """
        dL = DeferredList([])
        for wsID, instance in self.worldServers:
            def cb(stats):
                return wsID, stats
            dL.chainDeferred(instance.sendPacket().addCallback(cb))
        return dL

    def getWorldServerByWorldName(self, worldName):
        return self.db.runQuery("SELECT worldServerID FROM cb_worlds WHERE worldName = ?", worldName)

    # TODO Reuse this POS - What was I even thinking?
    def getOnlineWorldServerByWorldName(self, worldName):
        def cb(res):
            finalList = []
            for row in res:
                ws = row[0]
                # Check if it's online
                if ws in self.worldServers:
                    finalList.append(ws)
            return finalList
        return self.getWorldServerByWorldName(worldName).addCallback(cb)


    def leaveWorldServer(self, proto, wsID):
        """
        Leaves the current world server.
        """
        if not self.worldServers.has_key(wsID):
            raise KeyError("World server ID does not exist or is detached")
        self.worldServers[wsID].doLeaveServer(proto)