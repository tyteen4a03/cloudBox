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
from cloudbox.common.mixins import CloudBoxProtocolMixin, TickMixin


class WorldServerCommServerProtocol(Protocol, CloudBoxProtocolMixin, TickMixin):
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
        self.loops.registerLoop("packets", self.gpp.packetLoop).start(self.getTickInterval("outgoing-world"))

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
        d = self.sendPacket(TYPE_STATE_UPDATE,
            {
                "sessionID": sessionID,
                "clientState": states,
                "keysToDelete": keysToDelete
            },
        )
        if requireResponse:
            return d

    ### End-client related functions ###

    def protoDoJoinServer(self, proto, world=None):
        """
        Makes the protocol join the server.
        """
        toSend = {
            "playerID": proto.playerID,
            "username": proto.username,
            "ip": int(proto.ip),
        }
        if world:
            toSend["world"] = world
        # Send the basic information over
        d = self.sendClientStateUpdate(proto.sessionID, toSend, True)
        self.logger.info("Sent request for {} to join worldServer {}".format(proto.username, self.wsID))
        return d

    def protoDoLeaveServer(self, proto):
        """
        Makes the protocol leave the server.
        """
        pass