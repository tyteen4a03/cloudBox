# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol
from cloudbox.common.constants.handlers import *

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.logger import Logger
from cloudbox.common.mixins import CloudBoxProtocolMixin


class DatabaseClientProtocol(Protocol, CloudBoxProtocolMixin):
    """
    I am a Protocol for the DatabaseServer Client.
    """

    def __init__(self):
        # Requests waiting for a response from the DatabaseServer. Format: {requestID: callback}
        self.requests = {}

    ### Twisted methods ###

    def makeConnection(self, transport):
        self.logger = Logger()
        self.transport = transport
        self.ready = False  # Set to False to prevent new connections
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers)
        self.sendHandshake()

    def connectionMade(self):
        self.ready = True
        self.factory.instance = self

    def dataReceived(self, data):
        self.gpp.feed(data)
        self.gpp.parseFirstPacket()

    def connectionLost(self, reason):
        self.logger.error("Connection to Hub Server lost: {reason}".format(reason=reason))

    def sendDirectQuery(self, ):
        self.sendPacket(TYPE_DIRECT_QUERY, )

    @property
    def remoteServerType(self):
        return self.factory.remoteServerType