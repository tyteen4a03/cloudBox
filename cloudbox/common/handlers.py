# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import implements
from cloudbox.common.constants import common, handlers

from cloudbox.common.interfaces import IPacketHandler


class BasePacketHandler(object):
    """
    Base packet handler.
    """
    implements(IPacketHandler)

    def __init__(self, parent, logger):
        self.parent = parent
        self.logger = logger


class KeepAlivePacketHandler(BasePacketHandler):
    """
    A Handler class for keep-alive.
    """

    def packData(self, packetData):
        return "\x91\x00"  # This is static so might as well pre-pack it :D


class HandshakePacketHandler(BasePacketHandler):
    """
    A Handler class for packet HandshakeRequest.
    """

    def handleData(self, packetData):
        # See if they are in our allowed list
        if not self.parent.transport.getPeer().host in self.parent.factory.settings["main"]["allowed-ips"]:
            # Refuse connection
            self.parent.sendError("You are not connecting from an authorized IP.")
            self.parent.transport.loseConnection()
        if packetData[1] not in common.SERVER_TYPES:
            # Who are you?
            self.parent.sendError("Server type undefined.")
            self.parent.transport.loseConnection()

    def packData(self, packetData):
        return self.packer.pack([
            handlers.TYPE_HANDSHAKE,
            self.parent.serverName,
            self.parent.serverType
        ])


class DisconnectPacketHandler(BasePacketHandler):
    """
    A Handler class for Server Shutdown.
    """

    def handleData(self, packetData):
        # TODO ErrorID
        self.logger.info("{} closed connection, reason: {}".format(
            common.SERVER_TYPES_INV[packetData[0]], packetData[3]))
        if self.parent.remoteServerType == common.SERVER_TYPES["HubServer"]:
            # Hub Server is closing our connection, why oh why
            if self.parent.serverType == common.SERVER_TYPES["WorldServer"]:
                self.parent.factory.saveAllWorlds()
                self.parent.factory.closeAllWorlds()
            elif self.parent.serverType == common.SERVER_TYPES["DatabaseServer"]:
                return
        elif self.parent.remoteServerType == common.SERVER_TYPES["WorldServer"]:
            # World Server is closing our connection, probably shutting down
            self.parent.available = False
        self.parent.transport.loseConnection()

    def packData(self, packetData):
        return self.packer.pack([
            handlers.TYPE_DISCONNECT,
            self.parent.serverType, # In case the handshake failed
            packetData["disconnectType"],
            packetData["errorID"],
            packetData["message"]
        ])
