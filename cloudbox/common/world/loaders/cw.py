# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import logging
import shutil

import nbt.nbt as nbt
from zope.interface import implements

from cloudbox.common.constants.common import *
from cloudbox.world.exceptions import WorldLoadError
from cloudbox.world.interfaces import IWorldLoader


class ClassicWorldWorldLoader(object):
    implements(IWorldLoader)

    name = "ClassicWorld Format"
    supportsLoading = True
    supportsSaving = True

    worldStorageType = "file"
    fileExtensions = ["cw"]

    CURRENT_LEVEL_VERSION = 1

    ACCEPTABLE_LEVEL_VERSIONS = [1, ]

    requiredFields = {
        "Name": {
            "type": nbt.TAG_String,
            "default": ""
        },
        "FormatVersion": {
            "type": nbt.TAG_Byte,
            "default": 1
        },
        "UUID": {
            "type": nbt.TAG_Byte_Array,
            "default": None,  # Raise hell
        },
        "X": {
            "type": nbt.TAG_Short,
            "default": 0,
        },
        "Y": {
            "type": nbt.TAG_Short,
            "default": 0,
        },
        "Z": {
            "type": nbt.TAG_Short,
            "default": 0,
        },
        "Spawn": {
            "type": nbt.TAG_Compound,
            "default": {
                "X": {
                    "type": nbt.TAG_Short,
                    "default": 0,
                },
                "Y": {
                    "type": nbt.TAG_Short,
                    "default": 0,
                },
                "Z": {
                    "type": nbt.TAG_Short,
                    "default": 0,
                },
                "H": {
                    "type": nbt.TAG_Byte,
                    "default": 0,
                },
                "P": {
                    "type": nbt.TAG_Byte,
                    "default": 0,
                },
            }
        },
        "BlockArray": {
            "type": nbt.TAG_Byte_Array,
            "default": bytearray(),
        },
        "Metadata": {
            "type": nbt.TAG_Compound,
            "default": {
                "cloudBox": {
                    "type": nbt.TAG_Compound,
                    "default": {}
                }
            }
        }
    }
    optionalFields = {
        "CreatedBy": {
            "type": nbt.TAG_Compound,
            "default": {
                "Service": {
                    "type": nbt.TAG_String,
                    "default": "cloudBox"
                },
                "Username": {
                    "type": nbt.TAG_String,
                    "default": ""
                }
            }
        },
        "MapGenerator": {
            "type": nbt.TAG_Compound,
            "default": {
                "Software": {
                        "type": nbt.TAG_String,
                        "default": "cloudBox"
                    },
                "MapGeneratorName": {
                        "type": nbt.TAG_String,
                        "default": "cloudBox"
                    }
            }
        },
        "TimeCreated": {
            "type": nbt.TAG_Long,
            "default": 0
        },
        "LastAccessed": {
            "type": nbt.TAG_Long,
            "default": 0
        },
        "LastModified": {
            "type": nbt.TAG_Long,
            "default": 0
        }
    }

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger("cloudbox.world.loader.classicworld")

    def loadWorld(self, io=None):
        returnDict = {}

        if io is None:
            nbtObject = nbt.NBTFile(self.path, 'rb')
        else:
            nbtObject = nbt.NBTFile(fileobj=io)

        if nbtObject.name != "ClassicWorld":
            raise WorldLoadError(ERRORS["header_mismatch"], "Header mismatch. Maybe the file is broken?")
        if nbtObject["FormatVersion"].value not in self.ACCEPTABLE_LEVEL_VERSIONS:
            raise WorldLoadError(ERRORS["unsupported_level_version"], "Level version unsupported.")

        for r in self.requiredFields:
            if r not in nbtObject:
                self.logger.warn("Required field {} missing.".format(r))
                returnDict[r] = self.requiredFields[r]
            else:
                returnDict[r] = nbtObject[r]
        for r in self.optionalFields:
            if r in nbtObject:
                returnDict[r] = nbtObject[r]
            else:
                returnDict[r] = self.optionalFields[r]
        return returnDict

    def saveWorld(self, data, io=None):
        if io is None:
            nbtObject = nbt.NBTFile(self.path + ".tmp", 'wb')
        else:
            nbtObject = nbt.NBTFile(fileobj=io)

        for r in self.requiredFields:
            if r not in data:
                self.logger.warn("Required field {} missing.".format(r))
                nbtObject[r] = self.requiredFields[r]
            else:
                nbtObject[r] = data[r]
        for r in self.optionalFields:
            if r in data:
                nbtObject[r] = data[r]
            else:
                nbtObject[r] = self.optionalFields[r]
        nbtObject.write_file()
        shutil.move(self.path + ".tmp", self.path)