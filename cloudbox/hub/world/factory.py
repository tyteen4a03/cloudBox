# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ServerFactory

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.logger import Logger
from cloudbox.hub.world.protocol import WorldServerCommServerProtocol


class WorldServerCommServerFactory(ServerFactory):
    """
    I listen to World Servers and interact with them, acting as a proxy.
    """

    protocol = WorldServerCommServerProtocol
    remoteServerType = SERVER_TYPES["WorldServer"]

    def __init__(self, parentService):
        self.parentService = parentService
        self.worldServers = {}
        self.logger = Logger()

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def getServerType(self):
        return self.parentService.getServerType()

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_WORLD_SERVER.items())
        return h

    def getServerStats(self):
        """
        Gets the current load for each World Server and assemble them in a dict of {wsID: SLA}.
        """
        ret = {}
        for wsID, instance in self.worldServers:
            ret[wsID] = instance.getStats()["sla"]
        return ret

    def leaveWorldServer(self, proto, wsID):
        """
        Leaves the current world server.
        """
        if not self.worldServers.has_key(wsID):
            raise KeyError("World server ID does not exist or is detached")
        self.worldServers[wsID].doLeaveServer(proto)