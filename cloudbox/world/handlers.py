# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common, handlers

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.handlers import HandshakePacketHandler


class WorldHandshakePacketHandler(HandshakePacketHandler):
    def handleData(self, packetData):
        super(WorldHandshakePacketHandler, self).handleData(packetData)
        if packetData[1] == common.SERVER_TYPES["HubServer"]:
            # OK, connection established
            self.parent.logger.info("Connection with HubServer established.")


class StateUpdatePacketHandler(BasePacketHandler):
    def handleData(self, packetData):
        pass

    def packData(self, packetData):
        pass


class LoadWorldPacketHandler(BasePacketHandler):
    def handleData(self, packetData):
        pass

    def packData(self, packetData):
        return self.packer.pack([
            handlers.TYPE_LOAD_WORLD,
            packetData["worldID"],
            # Optional fields if hub wants the world to load the data from the database - not sure why anybody
            # would do this but oh well
            packetData["worldName"],
            packetData[""]
        ])