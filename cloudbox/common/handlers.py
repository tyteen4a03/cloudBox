# cloudBox is copyright 2012 - 2013 the cloudBox team.
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


class KeepAlivePacketHandler(BasePacketHandler):
    """
    A Handler class for keep-alive.
    """

    @classmethod
    def packData(cls, data):
        return "\x91\x00"  # This is static so might as well pre-pack it :D


class HandshakePacketHandler(BasePacketHandler):
    """
    A Handler class for packet HandshakeRequest.
    """

    @classmethod
    def handleData(cls, data):
        # See if they are in our allowed list
        if not data["parent"].transport.getPeer().host in data["parent"].factory.settings["main"]["allowed-ips"]:
            # Refuse connection
            data["parent"].sendError("You are not connecting from an authorized IP.")
            data["parent"].transport.loseConnection()
        if data["packetData"][1] not in common.SERVER_TYPES:
            # Who are you?
            data["parent"].sendError("Server type undefined.")
            data["parent"].transport.loseConnection()

    @classmethod
    def packData(cls, data):
        return data["packer"].pack([
            handlers.TYPE_HANDSHAKE,
            data["parent"].getServerName(),
            data["parent"].getServerType()
        ])


class DisconnectPacketHandler(BasePacketHandler):
    """
    A Handler class for Server Shutdown.
    """

    @classmethod
    def handleData(cls, data):
        data["logger"].info("{} closed connection, reason: {}".format(
            common.SERVER_TYPES_INV[data["packetData"][0]], data["packetData"][2]))
        if data["parent"].remoteServerType == common.SERVER_TYPES["HubServer"]:
            # Hub Server is closing our connection, why oh why
            if data["serverType"] == common.SERVER_TYPES["WorldServer"]:
                data["parent"].factory.saveAllWorlds()
                data["parent"].factory.closeAllWorlds()
            elif data["serverType"] == common.SERVER_TYPES["DatabaseServer"]:
                return
        elif data["parent"].remoteServerType == common.SERVER_TYPES["WorldServer"]:
            # World Server is closing our connection, probably shutting down
            data["parent"].available = False
        data["parent"].transport.loseConnection()

    @classmethod
    def packData(cls, data):
        return data["packer"].pack([
            handlers.TYPE_DISCONNECT,
            data["serverType"],
            data["disconnectType"],
            data["message"]
        ])
