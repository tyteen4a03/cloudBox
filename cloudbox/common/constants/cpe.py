# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants.classic import Format

TYPE_EXTINFO = 16
TYPE_EXTENTRY = 17

TYPE_FORMATS = {
    TYPE_EXTINFO: Format("sh"),
    TYPE_EXTENTRY: Format("si"),
}

CPE_EXTENSIONS = {
    "ClickDistance": {
        "ExtensionVersion": 1,
        "DefaultDistance": 160,
    },
    "CustomBlocks": {
        "ExtensionVersion": 1,
        "SupportLevel": 1,
        "Fallback": {
            1: {
                50: 44,
                51: 39,
                52: 12,
                53: 0,
                54: 10,
                55: 33,
                56: 25,
                57: 3,
                58: 29,
                59: 28,
                60: 20,
                61: 42,
                62: 49,
                63: 36,
                64: 5,
                65: 1,
            }
        }
    }
}