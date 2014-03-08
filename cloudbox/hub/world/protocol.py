# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxProtocolMixin


class WorldServerCommServerProtocol(Protocol, CloudBoxProtocolMixin):
    """
    The protocol class for the WorldServer communicator factory.
    """

    remoteServerType = SERVER_TYPES["WorldServer"]
    PACKET_LIMIT_NAME = "outgoing-world"

    def __init__(self):
        self.wsID = None
        self.logger = logging.getLogger("cloudbox.hub.world.protocol._default") # Will be replaced when we get a proper ID
        self.loops = LoopRegistry()

    def connectionMade(self):
        """
        Triggered when connection is established.
        """
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers, self.transport)
        self.loops.registerLoop("packets", self.setUpPacketLoop()).start(self.getTickInterval("outgoing-world"))

    def dataReceived(self, data):
        """
        Triggered when data is received.
        """
        # Pass on the data to the GPP
        # First, add the data we got onto our internal buffer
        self.gpp.feed(data)
        # Ask the GPP to decode the data, if possible
        self.gpp.parseFirstPacket()

    ### World Server related functions ###

    def getStats(self):
        # TODO
        return {
            "players": 0
        }

    ### Packet functions ###
    def sendClientStateUpdate(self, sessionID, states, keysToDelete=[], requireResponse=False):
        self.sendPacket(TYPE_STATE_UPDATE,
        {
            "sessionID": sessionID,
            "clientState": states,
            "keysToDelete": keysToDelete
        },

        )

    ### End-client related functions ###

    def protoDoJoinServer(self, proto, world=None):
        """
        Makes the protocol join the server.
        """
        toSend = ["playerID", "username", "ip"]
        # Send the basic information over
        self.sendClientStateUpdate(proto.sessionID, {
            "playerID": proto.playerID
        })
        self.logger.info("Sent request for {} to join worldServer {}".format(proto.username, self.wsID))

    def protoDoLeaveServer(self, proto):
        """
        Makes the protocol leave the server.
        """
        pass