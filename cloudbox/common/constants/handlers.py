# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

TYPE_KEEPALIVE = 0
TYPE_HANDSHAKE = 1
TYPE_STATEIDALLOCATION = 4
TYPE_STATEUPDATE = 4
TYPE_DISCONNECT = 255

# Handlers - the basics
# TODO Actually use this

# Packets sent from clients
HANDLERS_CLIENT_BASIC = {
    0x00: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    0x01: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    #0x02: "cloudbox.common.handlers", # Placeholder for encryption, unused for now
    0xFF: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}

# Packets sent from servers
HANDLERS_SERVER_BASIC = {
    0x00: ("cloudbox.common.handlers", "KeepAlivePacketHandler"),
    0x01: ("cloudbox.common.handlers", "HandshakePacketHandler"),
    #0x02: ["handshakeEncrypt", "cloudbox.common.handlers"], # Placeholder for encryption, unused for now
    0xFF: ("cloudbox.common.handlers", "DisconnectPacketHandler"),
}
HANDLERS_WORLD_SERVER = {
    0x04: ("cloudbox.world.handlers", "ClientStateIDAllocationPacketHandler"),
    0x05: ("cloudbox.world.handlers", "ClientStateUpdatePacketHandler")
}