# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common
from cloudbox.common.handlers import HandshakePacketHandler


class HubHandshakePacketHandler(HandshakePacketHandler):
    @classmethod
    def handleData(cls, data):
        super(HubHandshakePacketHandler, cls).handleData(data)
        if data["packetData"][1] == common.SERVER_TYPES["WorldServer"]:
            return
        elif data["packetData"][1] == common.SERVER_TYPES["DatabaseServer"]:
            dbClientFactory = data["parent"].getFactory("DatabaseClientFactory")
            if dbClientFactory.sentHandshake:
                dbClientFactory.ready = True
                data["parent"].parentService.loops.registerLoop("dbClientFactory.processRequests", dbClientFactory.processRequests).start(0.01)