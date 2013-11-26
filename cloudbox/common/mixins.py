# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *


class CloudBoxFactoryMixin(object):
    """
    A mixin class, providing common functions any cloudBox factories can expect.
    """

    parentService = None

    def getServerName(self):
        return self.settings["main"]["server-name"]

    def getServerType(self):
        return self.parentService.getServerType()

    def getFactory(self, factoryName):
        return self.parentService.factories[factoryName]


class CloudBoxProtocolMixin(object):
    """
    A mixin class, providing common functions any cloudBox protocols can expect.
    """

    def sendPacket(self, packetID, packetData={}):
        self.transport.write(self.gpp.packPacket(packetID, packetData))

    def sendHandshake(self):
        self.sendPacket(TYPE_HANDSHAKE)

    def sendError(self, error):
        self.sendDisconnect(DISCONNECT_ERROR, error)

    def sendServerShutdown(self, reason=""):
        self.sendDisconnect(DISCONNECT_SHUTDOWN, reason)

    def sendDisconnect(self, disconnectType=DISCONNECT_GENERIC, message=""):
        self.sendPacket(TYPE_DISCONNECT, {"disconnectType": disconnectType, "message": message})
