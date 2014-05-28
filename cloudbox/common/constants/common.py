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
    "no_results": 3,
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
    # DB errors
    "data_corrupt": 40,
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

SERVICES = {
    "Minecraft.net": 0,
    "ClassiCube": 1,
}

SERVICES_INV = dict((v, k) for k, v in SERVICES.iteritems())

ACTIONS = {
    "login": 0,
    "logout": 1,
    "register": 2,
    "verifyEmail": 3,
    "associate": 4,
    "editProfile": 5,  # Edit self
    "editWorld": 6,
    "editUser": 7,  # Edit others
    "ban": 8,
}

ACTIONS_INV = dict((v, k) for k, v in ACTIONS.iteritems())

BAN_TYPES = {
    "globalBan": 0,
    "globalIPBan": 1,
    "worldBan": 2,
    "worldIPBan": 3
}

BAN_TYPES_INV = dict((v, k) for k, v in BAN_TYPES.iteritems())

import uuid

UUID = {
    "cloudbox": uuid.UUID("141361c5-3bea-49e4-bf9f-89b01ba74e2a"),
    "cloudbox.servers": uuid.UUID('791a2ef0-fe5f-5ce0-b00a-0d9c11ff49ab'),
    "cloudbox.worlds": uuid.UUID('c6b37b83-26a5-51fc-b078-adc6e388a9a3'),
    "cloudbox.users": uuid.UUID('b0a6eda6-dad3-5cd6-ad2d-3b3ff28429c9'),
    "cloudbox.userGroups": uuid.UUID('baf304c4-4db2-5421-a8b5-fbf7849d9fc0'),
}