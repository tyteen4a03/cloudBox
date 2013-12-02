# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol
from twisted.python.failure import Failure
from cloudbox.common.constants.handlers import *

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.mixins import CloudBoxProtocolMixin


class DatabaseServerProtocol(Protocol, CloudBoxProtocolMixin):
    """
    Protocol for DatabaseServer.
    """

    def __init__(self):
        self.requests = dict()
        self.gpp = None
        self.remoteServerType = None
        self.requests = dict()

    def connectionMade(self):
        """
        Triggered when connection is established.
        """
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers)

    def dataReceived(self, data):
        """
        Triggered when data is received.
        """
        # Pass on the data to the GPP
        # First, add the data we got onto our internal buffer
        self.gpp.feed(data)
        # Ask the GPP to decode the data, if possible
        self.gpp.parseFirstPacket()

    def standardQueryCallback(self, res, requestID):
        if isinstance(res, Failure):
            # Oh noes!
            self.sendQueryResult(requestID, False, res.getErrorMessage())
        else:
            self.sendQueryResult(requestID, True, res.fetchall())
        # Find the request entry
        entry = self.factory.request[requestID]
        # Drop the entry from the protocol, then drop it from the master
        del entry["protocol"].requests[entry["remoteRequestID"]]
        del self.factory.request[requestID]

    def sendQueryResult(self, requestID, result, resource):
        """
        Sends the query result.

        @param requestID int The request ID.
        @param result bool The result of the operation.
        @param resource mixed The resource fetched from the operation, or a failure message.
        """
        self.sendPacket(TYPE_QUERY_RESULT, {"requestID": requestID, "result": result, "resource": resource})
