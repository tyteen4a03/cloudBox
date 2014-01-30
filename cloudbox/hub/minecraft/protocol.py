# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone as _connDone

from cloudbox.common.constants.classic import *
from cloudbox.common.constants.common import *
from cloudbox.common.gpp import MinecraftClassicPacketProcessor
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.mixins import CloudBoxProtocolMixin
from cloudbox.hub.exceptions import WorldServerLinkException


class MinecraftHubServerProtocol(Protocol, CloudBoxProtocolMixin):
    """
    Main protocol class for communicating with clients.
    """

    def __init__(self):
        self.playerID = None # UID, stored in DB
        self.sessionID = None # Session ID, used to communicate between client and server
        self.ip = None
        self.gpp = None
        self.username = None
        self.wsID = None  # World Server this user belongs to
        self.identified = False
        self.state = {}  # A special dict used to hold temporary "signals"
        self.logger = logging.getLogger("cloudbox.hub.mc.protocol._default") # This will be replaced once we get a proper ID

    ### Twisted Methods ###

    def connectionMade(self):
        """
        Called when a connection is made.
        """
        # Get an ID for ourselves
        self.sessionID = self.factory.claimID(self)
        if self.sessionID is None:
            self.sendError("The server is full.")
            return
        self.ip = self.transport.getPeer().host
        self.logger = logging.getLogger("cloudbox.hub.mc.protocol.{}".format(self.sessionID))
        self.gpp = MinecraftClassicPacketProcessor(self, self.factory.handlers)

    def connectionLost(self, reason=_connDone):
        # Leave the world
        self.factory.leaveWorldServer(self, self.wsID)
        # Release our ID
        self.factory.releaseID(self.sessionID)

    def dataReceived(self, data):
        """
        Called when data is received.
        """
        # Add the data we got onto our internal buffer
        self.gpp.feed(data)
        self.logger.debug(data)
        self.gpp.parseFirstPacket()

    ### Message Handling ###

    def send(self, msg):
        """
        Sends raw data to the client.
        """
        self.transport.write(msg)

    def sendPacket(self, packetID, packetData={}):
        self.transport.write(self.gpp.packPacket(packetID, packetData))

    def sendError(self, error, disconnectNow=False):
        """
        Sends an error the client.
        """
        self.factory.logger.info("Sending error: %s" % error)
        self.sendPacket(TYPE_ERROR, {"error": error})
        if disconnectNow:
            self.transport.loseConnection()
        else:
            reactor.callLater(0.2, self.transport.loseConnection)

    def sendMessage(self, message):
        """
        Sends a message to the client.
        """
        self.sendPacket(TYPE_MESSAGE, {"message": message})

    def sendChanneledMessage(self, message, channel):
        """
        Sends a message that has a channel.
        """
        self.sendMessage(message)

    def sendServerMessage(self, message, channel=None):
        """
        Shortcut for sending a server-like messgae to the client (yellow messgaes)
        """
        self.sendChanneledMessage(COLOUR_YELLOW + message, channel=None)

    def sendKeepAlive(self):
        """
        Sends a ping to the client.
        """
        self.sendPacket(TYPE_KEEPALIVE, {})

    def sendBlock(self, x, y, z, block=None):
        """
        Sends a block.
        """
        if block is not None:
            self.sendPacket(TYPE_BLOCKSET, {"x": x, "y": y, "z": z, "block": block})
        else:
            # Ask the World Server to get the block, and send it.
            # TODO
            return

    ### Relay ###

    def relayClientData(self, handlerID, data):
        pass

    ### Actions  ###

    def _joinWorldFailedErrback(self, err):
        """
        Callback for when world joining failed
        """
        if self.world is None:  # We are newbies
            self.sendError("World loading failed - {}".format(str(err)))
        else:
            self.sendServerMessage("World loading failed - {}".format(str(err)))
        # Cancel any stuff if needed to

    def joinDefaultWorld(self):
        """
        Joins the default world.
        """
        mode = self.factory.settings["main"]["entry-mode"]
        if mode == "solo":
            # Find out which WS has the default world and join it
            def afterGetDefaultWorld(res):
                row = res.fetch_row()
                wsf = self.factory.getFactory("WorldServerCommServerFactory")
                # Get world server link
                if row[3] not in wsf.worldServers:
                    # WorldServer down, raise hell
                    raise WorldServerLinkException
                # Send the player over
                wsf.worldServers[row[3]].protoDoJoinServer(world=row[3])
            self.db.runQuery("SELECT worldName, worldID, worldPath, wsID FROM cb_worlds WHERE isDefault=1")\
                .addCallbacks(afterGetDefaultWorld, self._joinWorldFailedErrback)
        elif mode == "distributed":
            # Find out which WS has the default world and join any of them.
            self.otherThings()

    def joinWorldServer(self, wsID):
        """
        Joins a World Server given its ID.
        """
        pass

    def leaveWorldServer(self, wsID):
        """
        Leaves the current worldServer.
        """
        self.getFactory("WorldServerCommServerFactory").leaveWorldServer(self, wsID)