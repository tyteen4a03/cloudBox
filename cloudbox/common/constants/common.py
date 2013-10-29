# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

VERSION = "1.0.0 Alpha 1"
# 2 Major, 2 Minor, 2 Minor, 1 ReleaseType, 1 ReleaseVersion
# 0 = Alpha, 1 = Beta, 2 = RC, 3 = Release, 4 = Post-release hotfixes
VERSION_NUMBER = 01000001

# Server types

SERVER_TYPES = {
    "HubServer": 0,
    "WorldServer": 1,
    "DatabaseServer": 2,
    "HeartbeatService": 3,
}

SERVER_TYPES_INV = dict((v, k) for k, v in SERVER_TYPES.iteritems())

DEFAULT_PERMISSIONS = {

}

# Errors

ERR_NOT_ENOUGH_DATA = 100
ERR_METHOD_NOT_FOUND = 101
ERR_UNABLE_TO_PARSE_DATA = 102

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

