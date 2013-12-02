# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.handlers import HandshakePacketHandler


class WorldHandshakePacketHandler(HandshakePacketHandler):
    @classmethod
    def handleData(cls, data):
        super(WorldHandshakePacketHandler, cls).handleData(data)
        if data["packetData"][1] == common.SERVER_TYPES["WorldServer"]:
            return



class StateUpdatePacketHandler(BasePacketHandler):
    @classmethod
    def handleData(cls, data):
        pass

    @classmethod
    def packData(cls, data):
        pass