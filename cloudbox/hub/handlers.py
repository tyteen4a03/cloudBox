# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants import common
from cloudbox.common.database import hasFailed
from cloudbox.common.handlers import HandshakePacketHandler
from cloudbox.common.models.servers import WorldServer


class HubHandshakePacketHandler(HandshakePacketHandler):
    def handleData(self, packetData, requestID=None):
        super(HubHandshakePacketHandler, self).handleData(packetData, 0)
        if packetData[1] == common.SERVER_TYPES["WorldServer"]:
            # See if they are on our allowed list
            if self.parent.transport.getPeer().host not in self.parent.factory.settings["main"]["allowed-ips"]:
                self.parent.sendError("IP not in allowed list. Check config?")

            # Get the worldServerID from the database
            def afterGetWSID(res):
                hasFailed(res)
                if not res:
                    raise
                self.parent.factory.worldServers[res[0]["id"]] = self.parent
                self.parent.sendHandshake(res[0]["id"])
                self.parent.id = res[0]["id"]
                self.parent.connectionEstablished = True

            self.parent.db.runQuery(
                *WorldServer.select().where(WorldServer.name == packetData[0]).sql()
            ).addBoth(afterGetWSID)