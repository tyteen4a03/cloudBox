# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

# 0x0, 1, 2 are reserved for globally used packets,
# 0x3, 4 are reserved for world servers,
# 0x5, 6 are reserved for database servers,
# 0x7, 8, 9 are reserved for web servers.
# 0xF are reserved for exception handling (shared globally)

TYPE_KEEPALIVE = 0x00
TYPE_HANDSHAKE = 0x01

TYPE_STATEID_ALLOCATION = 0x30
TYPE_STATE_UPDATE = 0x31
TYPE_LOAD_WORLD = 0x32

TYPE_FETCH_DATA = 0x50
TYPE_DIRECT_QUERY = 0x51  # Use FetchData whenever possible. Should only be used for complex queries and/or testing only.
TYPE_QUERY_RESULT = 0x52

TYPE_ERROR = 0xFE
TYPE_DISCONNECT = 0xFF

# Handlers - the basics

# Packets sent from clients
HANDLERS_CLIENT_BASIC = {
    TYPE_KEEPALIVE: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    TYPE_HANDSHAKE: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    #0x02: "cloudbox.common.handlers", # Placeholder for encryption, unused for now
    TYPE_ERROR: ("cloudbox.common.handlers", "ErrorPacketHandler"),
    TYPE_DISCONNECT: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}

# Packets sent from servers
HANDLERS_SERVER_BASIC = {
    TYPE_KEEPALIVE: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    TYPE_HANDSHAKE: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    #0x02: ["handshakeEncrypt", "cloudbox.common.handlers"], # Placeholder for encryption, unused for now
    TYPE_ERROR: ("cloudbox.common.handlers", "ErrorPacketHandler"),
    TYPE_DISCONNECT: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}
HANDLERS_WORLD_SERVER = {
    TYPE_STATEID_ALLOCATION: ("cloudbox.world.handlers", "ClientStateIDAllocationPacketHandler"),
    TYPE_STATE_UPDATE: ("cloudbox.world.handlers", "ClientStateUpdatePacketHandler"),
    TYPE_LOAD_WORLD: ("cloudbox.world.handlers", "LoadWorldPacketHandler")
}

HANDLERS_DATABASE_SERVER = {
    #TYPE_FETCH_DATA: ("cloudbox.database.handlers", "FetchDataPacketHandler"), # Not until peewee-twisted is ready
    TYPE_DIRECT_QUERY: ("cloudbox.database.handlers", "DirectQueryPacketHandler"),
    TYPE_QUERY_RESULT: ("cloudbox.database.handlers", "QueryResultPacketHandler"),
}

# Future consideration: Unused for now

#from collections import namedtuple


class namedtuple(object):
    def __init__(self, *args, **kwargs):
        pass

# Packet definition
BASE_PACKET = namedtuple("Packet", ["packetID", "packetData"])

PACKET_DEFS = {}

PACKET_DEFS[TYPE_KEEPALIVE] = namedtuple("KeepAlivePacket", [])
PACKET_DEFS[TYPE_HANDSHAKE] = namedtuple("HandshakePacket", ["serverName", "serverType"])
PACKET_DEFS[TYPE_STATEID_ALLOCATION] = namedtuple("StateIDAllocationPacket", ["requestID", ""])
PACKET_DEFS[TYPE_STATE_UPDATE] = namedtuple("StateUpdatePacket", ["playerID", "updates"])
PACKET_DEFS[TYPE_LOAD_WORLD] = namedtuple("LoadWorldPacket", [])
PACKET_DEFS[TYPE_FETCH_DATA] = namedtuple("FetchDataPacket", [])
PACKET_DEFS[TYPE_DIRECT_QUERY] = namedtuple("DirectQueryPacket", [])
PACKET_DEFS[TYPE_QUERY_RESULT] = namedtuple("QueryResultPacket", [])
PACKET_DEFS[TYPE_ERROR] = namedtuple("ErrorPacket", [])
PACKET_DEFS[TYPE_DISCONNECT] = namedtuple("DisconnectPacket", [])