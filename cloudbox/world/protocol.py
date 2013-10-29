# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from msgpack import Packer
from twisted.internet.protocol import Protocol

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.handlers import *
from cloudbox.common.logger import Logger
from cloudbox.world.handlers import *


class WorldServerProtocol(Protocol):
    """
    I am a Protocol for the World Server.
    """

    ### Twisted-related functions ###

    def makeConnection(self, transport):
        self.logger = Logger()
        self.transport = transport
        self.available = False  # Set to False to prevent new connections
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers)
        self.sendHandshake()

    def connectionMade(self):
        self.available = True
        self.factory.instance = self

    def connectionLost(self, reason):
        self.logger.error("Connection to Hub Server lost: {reason}".format(reason=reason))

    def getServerType(self):
        return self.factory.getServerType()

    def getServerName(self):
        return self.factory.getServerName()

    @property
    def remoteServerType(self):
        return self.factory.remoteServerType

    def dataReceived(self, data):
        self.gpp.feed(data)
        self.gpp.parseFirstPacket()

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