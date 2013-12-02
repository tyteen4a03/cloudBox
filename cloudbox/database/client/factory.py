# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ReconnectingClientFactory

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.logger import Logger
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxFactoryMixin
from cloudbox.database.client.protocol import DatabaseClientProtocol


class DatabaseClientFactory(ReconnectingClientFactory, CloudBoxFactoryMixin):
    protocol = DatabaseClientProtocol
    retryConnection = False
    remoteServerType = SERVER_TYPES["DatabaseServer"]

    def __init__(self, parentService):
        self.parentService = parentService
        self.logger = Logger()
        self.loops = LoopRegistry()
        # Request dict format:
        # requestID:
        #   type: 0 = model, 1 = direct
        #   extraParameters: extra parameters for remote to run runQuery/Interaction as.
        #   isOperation: bool - Specify this to not call you back
        #   callback: func - Method to call when result is received from database server.
        #   if type is 0:
        #     model: a Populated model class.
        #   if type is 1:
        #     query: A query.
        #     interpolation: Parameters to replace placeholders.
        self.requests = dict()
        self.sentRequests = dict()  # RequestID: callbackFunction
        self.instance = None
        self.retryConnection = True

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_DATABASE_SERVER.items())
        h[TYPE_HANDSHAKE] = ("cloudbox.database.handlers", "DatabaseClientPacketHandler")
        return h

    def processRequests(self):
        rIter = self.requests.iteritems()
        cur = 0
        try:
            while cur < self.parentService.settings["common"]["requests-per-tick"]["dbclient-outgoing"]:
                requestID, requestData = rIter.next()

                if requestData["type"] == 1:
                    self.instance.sendDirectQuery()
                else:
                    self.instance.sendFetchData()
                self.sentRequests[requestID] = requestData["callback"]
        except StopIteration:
            # Okay, we're done here.
            self.logger.debug("{requests} outgoing database request processed.".format(requests=cur))

    ### Twisted functions ###

    def buildProtocol(self, addr):
        self.resetDelay()
        proto = DatabaseClientProtocol()
        proto.factory = self
        return proto

    def quit(self, msg):
        self.retryConnection = False
        # Tell the HubServer we are breaking up
        self.instance.sendDisconnect()

    def clientConnectionLost(self, connector, reason):
        """
        If we get disconnected, reconnect to server.
        """
        self.instance = None
        if self.rebootFlag:
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.logger.critical("Connection to DatabaseServer failed: %s" % reason)
        connector.connect()