# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from msgpack import Packer

from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxProtocolMixin, TickMixin


class WorldServerProtocol(Protocol, CloudBoxProtocolMixin, TickMixin):
    """
    I am a Protocol for the World Server.
    """

    PACKET_LIMIT_NAME = "outgoing"

    ### Twisted-related functions ###

    def __init__(self, logger):
        self.logger = logger
        self.ready = False  # Set to False to prevent new connections
        self.loops = LoopRegistry()

    def connectionMade(self):
        self.factory.instance = self
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers, self.transport)
        self.loops.registerLoop("packets", self.gpp.packetLoop).start(self.getTickInterval("outgoing"))
        self.logger.info("Connecting to Hub Server...")
        self.sendHandshake()
        self.ready = True

    def dataReceived(self, data):
        self.gpp.feed(data)
        self.gpp.parseFirstPacket()

    def connectionLost(self, reason):
        self.logger.error("Connection to Hub Server lost: {reason}".format(reason=reason))

    @property
    def remoteServerType(self):
        return self.factory.remoteServerType