# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common, handlers

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.handlers import HandshakePacketHandler
from cloudbox.common.player import Player


class WorldHandshakePacketHandler(HandshakePacketHandler):
    def handleData(self, packetData, requestID=None):
        super(WorldHandshakePacketHandler, self).handleData(packetData, requestID)
        if packetData[1] == common.SERVER_TYPES["HubServer"]:
            # OK, connection established
            self.parent.factory.id = packetData[2]
            self.parent.connectionEstablished = True
            self.logger.info("Connection with HubServer established.")


class NewPlayerPacketHandler(BasePacketHandler):
    packetID = handlers.TYPE_NEW_PLAYER

    def handleData(self, packetData, requestID=None):
        sessionID = packetData[0]
        thePlayer = Player()
        thePlayer["sessionID"] = sessionID
        self.parent.factory.clients[sessionID] = thePlayer
        if requestID > 0:
            self.parent.sendCallback(requestID, True)

    def packData(self, packetData):
        return [packetData["sessionID"]]


class PlayerDisconnectPacketHandler(BasePacketHandler):
    packetID = handlers.TYPE_PLAYER_DISCONNECT

    def handleData(self, packetData, requestID=None):
        sessionID = packetData[0]
        # Cleanup here
        del self.parent.factory.clients[sessionID]
        if requestID > 0:
            self.parent.sendCallback(requestID, True)

    def packData(self, packetData):
        return [packetData["sessionID"]]


class StateUpdatePacketHandler(BasePacketHandler):
    packetID = handlers.TYPE_STATE_UPDATE

    def handleData(self, packetData, requestID=None):
        if len(packetData) == 1:
            # Delete whatever we have
            del self.parent.factory.clients[packetData[0]]
            return
        if packetData[0] not in self.parent.factory.clients:
            self.parent.factory.clients[packetData[0]] = Player()
        self.parent.factory.clients[packetData[0]].update(packetData[1])
        if len(packetData) == 3:
            for key in packetData[2]:
                del self.parent.factory.clients[packetData[0]][key]
        if len(packetData) > 2:
            for key, value in packetData[1].iteritems():
                self.parent.factory.clients[packetData[0]][key] = value
        # Callback if needed
        if requestID > 0:
            self.parent.sendCallback(requestID, True)

    def packData(self, packetData):
        l = [packetData["sessionID"]]
        if packetData["clientState"]:
            # If we are not clearing the opposite side's data
            l.append(packetData["clientState"])
        if packetData["keysToDelete"]:
            l.append(packetData["keysToDelete"])
        return l


class LoadWorldPacketHandler(BasePacketHandler):
    packetID = handlers.TYPE_LOAD_WORLD

    def handleData(self, packetData, requestID=None):
        def afterWorldLoaded():
            if requestID > 0:
                self.parent.sendCallback(requestID, True)

        def afterWorldLoadFail():
            if requestID > 0:
                self.parent.sendCallback(requestID, False)

    def packData(self, packetData):
        return [
            packetData["worldID"],
            # Optional fields if hub wants the world to load the data from the database - not sure why anybody
            # would do this but oh well
            packetData["worldName"],
            packetData["worldFilename"]
        ]