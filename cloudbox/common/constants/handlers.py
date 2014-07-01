# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

# 0x0, 1, 2 are reserved for globally used packets,
# 0x3, 4 are reserved for world servers,
# 0x5, 6 are reserved for web servers.
# 0xF are reserved for exception handling (shared globally)

TYPE_KEEPALIVE = 0x00
TYPE_HANDSHAKE = 0x01
TYPE_GET_STATUS = 0x02
TYPE_CALLBACK = 0x03

TYPE_STATE_UPDATE = 0x30
TYPE_NEW_PLAYER = 0x31
TYPE_PLAYER_DISCONNECT = 0x32
TYPE_LOAD_WORLD = 0x33

TYPE_ERROR = 0xFE
TYPE_DISCONNECT = 0xFF

# Handlers - the basics

# Packets sent from clients
HANDLERS_CLIENT_BASIC = {
    TYPE_KEEPALIVE: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    TYPE_HANDSHAKE: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    TYPE_CALLBACK: ("cloudbox.common.handlers", "CallbackPacketHandler"),
    TYPE_ERROR: ("cloudbox.common.handlers", "ErrorPacketHandler"),
    TYPE_DISCONNECT: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}

# Packets sent from servers
HANDLERS_SERVER_BASIC = {
    TYPE_KEEPALIVE: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    TYPE_HANDSHAKE: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    TYPE_CALLBACK: ("cloudbox.common.handlers", "CallbackPacketHandler"),
    TYPE_ERROR: ("cloudbox.common.handlers", "ErrorPacketHandler"),
    TYPE_DISCONNECT: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}

HANDLERS_WORLD_SERVER = {
    TYPE_STATE_UPDATE: ("cloudbox.world.handlers", "StateUpdatePacketHandler"),
    TYPE_NEW_PLAYER: ("cloudbox.world.handlers", "NewPlayerPacketHandler"),
    TYPE_PLAYER_DISCONNECT: ("cloudbox.world.handlers", "PlayerDisconnectPacketHandler"),
    TYPE_LOAD_WORLD: ("cloudbox.world.handlers", "LoadWorldPacketHandler")
}

TASKS_GLOBAL = {

}
TASKS_HUB_MC = {

}