# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common, handlers

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.handlers import HandshakePacketHandler


class WorldHandshakePacketHandler(HandshakePacketHandler):
    def handleData(self, packetData, requestID=None):
        super(WorldHandshakePacketHandler, self).handleData(packetData, requestID)
        if packetData[1] == common.SERVER_TYPES["HubServer"]:
            # OK, connection established
            self.parent.connectionEstablished = True
            self.logger.info("Connection with HubServer established.")


class StateUpdatePacketHandler(BasePacketHandler):
    packetID = handlers.TYPE_STATE_UPDATE

    def handleData(self, packetData, requestID=None):
        if len(packetData) == 1:
            # Delete whatever we have
            del self.parent.factory.clients[packetData[0]]
            return
        self.parent.factory.clients[packetData[0]].update(packetData)
        if len(packetData) == 3:
            for key in packetData[2]:
                del self.parent.factory.clients[packetData[0]][key]
        if len(packetData) > 2:
            for key, value in packetData[1].iteritems():
                self.parent.factory.clients[packetData[0]][key] = value
        # Callback if needed
        if requestID > 0:
            self.gpp.sendPacket(handlers.TYPE_CALLBACK, {"isSuccess": True})

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
        pass

    def packData(self, packetData):
        return [
            packetData["worldID"],
            # Optional fields if hub wants the world to load the data from the database - not sure why anybody
            # would do this but oh well
            packetData["worldName"],
            packetData["worldFilename"]
        ]