# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from twisted.internet.protocol import ReconnectingClientFactory

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.database import hasFailed
from cloudbox.common.exceptions import DatabaseServerLinkException
from cloudbox.common.mixins import CloudBoxFactoryMixin, TaskTickMixin
from cloudbox.common.models.world import World
from cloudbox.world.protocol import WorldServerProtocol


class WorldServerFactory(ReconnectingClientFactory, CloudBoxFactoryMixin, TaskTickMixin):
    """
    I am the world server. I host some worlds, and do calculations about them.
    """
    protocol = WorldServerProtocol
    retryConnection = False
    remoteServerType = SERVER_TYPES["HubServer"]

    IS_CLIENT = True

    def __init__(self, parentService):
        self.parentService = parentService
        self.logger = logging.getLogger("cloudbox.world.factory")
        self.worlds = []
        self.clients = {}  # {clientID: clientStates} - clientID: player ID, clientStates: dict of states
        self.id = None
        self.instance = None
        self.retryConnection = True

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_WORLD_SERVER.items())
        h[TYPE_HANDSHAKE] = ("cloudbox.world.handlers", "WorldHandshakePacketHandler")
        return h

    ### Twisted functions

    def buildProtocol(self, addr):
        self.resetDelay()
        proto = WorldServerProtocol(self.logger)
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
        if self.retryConnection:
            self.logger.error("Connection to HubServer lost. Trying again...")
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.logger.critical("Connection to HubServer failed: %s" % reason)
        connector.connect()

    def loadWorld(self, worldInfo):
        """
        Loads the world given a World database entry.
        :param worldInfo A world database entry.
        """
        # Find the world class to use according to its type

    def loadWorldByID(self, worldID):
        """
        Loads the world given the ID.
        """
        def afterWorldSelect(res):
            if hasFailed(res):
                raise
            self.loadWorld(res[0])
        self.db.runQuery(*World.select().where(World.id == worldID).sql()).addCallback(afterWorldSelect)

    def loadWorldByWorldName(self, worldName):
        """
        Loads the world given its name
        :param worldName The world name.
        :return int World ID.
        """
        def afterWorldSelect(res):
            if hasFailed(res):
                raise
            self.loadWorld(res[0])
        self.db.runQuery(*World.select().where(World.name == worldName).sql()).addCallback(afterWorldSelect)

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

    def saveAllWorlds(self):
        """
        Saves all worlds.
        """
        # TODO Return the Deferreds?
        for w in self.worlds:
            w.saveWorld()

    def closeWorld(self, worldID):
        """
        Closes a world without saving its states.
        :param worldID The world ID.
        """
        w = self.worlds[worldID]
        # TODO Some physics shutdown logic here

    def closeAllWorlds(self):
        """
        Close all worlds.
        """
        for w in self.worlds:
            self.closeWorld(w.worldID)

    def addWorld(self, worldName, filepath):
        """Adds the world to the database."""
        self.db.runQuery()

    def deleteWorld(self, worldID):
        self.db.runQuery()