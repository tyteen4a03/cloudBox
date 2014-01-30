# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

VERSION = "1.0.0 Alpha 1"
# 1 Major, 2 Minor, 2 Minor, 1 ReleaseType, 1 ReleaseVersion
# 1 = Alpha, 2 = Beta, 3 = RC, 4 = Release, 5 = Post-release hotfixes
VERSION_NUMBER = 1000011

# Server types

SERVER_TYPES = {
    "HubServer": 0,
    "WorldServer": 1,
    "WebServer": 2,
    "HeartbeatService": 3,
}

SERVER_TYPES_INV = dict((v, k) for k, v in SERVER_TYPES.iteritems())

# Because I am horribly lazy
SERVER_TYPES_ABBRV = {
    "hub": 0,
    "world": 1,
    "web": 2,
    "hbservice": 3,
}

SERVER_TYPES_ABBRV_INV = dict((v, k) for k, v in SERVER_TYPES_ABBRV.iteritems())

DEFAULT_PERMISSIONS = {

}

# Errors
ERRORS = {
    # The very very generic errors
    "unknown": 0,
    "ioerror": 1,
    "connection_lost": 2,
    # Generic server link
    "connection_refused": 10,
    # GPP
    "not_enough_data": 20,
    "handler_not_found": 21,
    "corrupt_data": 22,
    # World loader
    "header_mismatch": 30,
    "unsupported_level_version": 31,
    "required_fields_missing": 32,
    # Hub <-> World methods error
    "worldserver_link_not_established": 200,
    "world_file_not_found": 201
}

ERRORS_INV = dict((v, k) for k, v in ERRORS.iteritems())

# Disconnect types
DISCONNECT_GENERIC = 0
DISCONNECT_SHUTDOWN = 1
DISCONNECT_ERROR = 2

# Format Lengths - used in Format

FORMAT_LENGTHS = {
    "b": 1,
    "a": 1024,
    "s": 64,
    "h": 2,
    "i": 4,
}

# Colours in MC

COLOUR_BLACK = "&0"
COLOUR_DARKBLUE = "&1"
COLOUR_DARKGREEN = "&2"
COLOUR_DARKCYAN = "&3"
COLOUR_DARKRED = "&4"
COLOUR_DARKPURPLE = "&5"
COLOUR_DARKYELLOW = "&6"
COLOUR_GREY = "&7"
COLOUR_DARKGREY = "&8"
COLOUR_BLUE = "&9"
COLOUR_GREEN = "&a"
COLOUR_CYAN = "&b"
COLOUR_RED = "&c"
COLOUR_PURPLE = "&d"
COLOUR_YELLOW = "&e"
COLOUR_WHITE = "&f"

