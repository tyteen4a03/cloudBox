# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common
from cloudbox.common.handlers import HandshakePacketHandler


class HubHandshakePacketHandler(HandshakePacketHandler):
    def handleData(self, packetData, requestID=0):
        super(HubHandshakePacketHandler, self).handleData(packetData, 0)
        if packetData[1] == common.SERVER_TYPES["WorldServer"]:
            # See if they are on our allowed list
            if self.parent.transport.getPeer().host not in self.parent.factory.settings["main"]["allowed-ips"]:
                self.parent.sendError("IP not in allowed list. Check config?")