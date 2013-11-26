# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ReconnectingClientFactory

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.logger import Logger
from cloudbox.common.mixins import CloudBoxFactoryMixin
from cloudbox.world.protocol import WorldServerProtocol


class WorldServerFactory(ReconnectingClientFactory, CloudBoxFactoryMixin):
    """
    I am the world server. I host some worlds, and do calculations about them.
    """
    protocol = WorldServerProtocol
    retryConnection = False
    remoteServerType = SERVER_TYPES["HubServer"]

    def __init__(self, parentService):
        self.parentService = parentService
        self.logger = Logger()
        self.worlds = []
        self.clients = {}  # {clientID: client ID (assigned by HubServer), clientStates: dict of states}
        self.instance = None
        self.retryConnection = True

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_WORLD_SERVER.items())
        return h

    ### Twisted functions

    def buildProtocol(self, addr):
        self.resetDelay()
        proto = WorldServerProtocol()
        proto.factory = self
        return proto

    def quit(self, msg):
        self.retryConnection = False
        # Tell the HubServer we are breaking up
        self.instance.sendDisconnect()

    def clientConnectionLost(self, connector, reason):
        """
        If we get disconnected, reconnect to server.
        """
        self.instance = None
        if self.rebootFlag:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.logger.critical("Connection to HubServer failed: %s" % reason)
        connector.connect()

    def loadWorld(self, worldId=None):
        """
        Load the world given the ID.
        If no ID is given, automatically generate one.
        """


    def _loadWorld(self, filepath):


    def unloadWorld(self, worldId):
        pass

    def packWorld(self, worldId):
        """
        Packs the world as a world stream to be sent to Hub Server.
        """
        pass

    def unpackWorld(self, worldStream):
        """
        Unpacks the world stream sent from the Hub server.
        """
        pass

    def saveWorld(self, worldID):
        pass

    def saveAllWorlds(self):
        pass

    def closeWorld(self, worldID):
        pass

    def closeAllWorlds(self):
        pass

    def addWorld(self, worldName, filepath):
        """Adds the world to the database."""
        self.dbConnector.

    def deleteWorld(self, worldID):