# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from pynbt.nbt import BaseTag
from cloudbox.common.util import walkDictWithRef

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import gzip
import logging
import shutil

from pynbt import *
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

    # Field definiton: itemName: default

    requiredFields = {
        "Name": TAG_String(""),
        "FormatVersion": TAG_Byte(1),
        "UUID": TAG_Byte_Array(bytearray()),
        "X": TAG_Short(0),
        "Y": TAG_Short(0),
        "Z": TAG_Short(0),
        "Spawn": {
            "X": TAG_Short(0),
            "Y": TAG_Short(0),
            "Z": TAG_Short(0),
            "H": TAG_Byte(0),
            "P": TAG_Byte(0),
        },
        "BlockArray": TAG_Byte_Array(bytearray()),
        "Metadata": {
            "cloudBox": {},
        }
    }
    optionalFields = {
        "CreatedBy": {
            "Service": TAG_String("ClassiCube"),
            "Username": TAG_String(""),
        },
        "MapGenerator": {
            "Software": TAG_String("cloudBox"),
            "MapGeneratorName": TAG_String("cloudBox"),
        },
        "TimeCreated": TAG_Long(0),
        "LastAccessed": TAG_Long(0),
        "LastModified": TAG_Long(0),
    }

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger("cloudbox.world.loader.classicworld")

    def _loadRequired(self, d, rd, k, v):
        if k not in d:
            self.logger.warn("Required field {} missing.".format(k))
            return k, rd[k].value if isinstance(rd[k], BaseTag) else rd[k]
        else:
            return k, v.value if isinstance(v, BaseTag) else v

    def _loadOptional(self, d, rd, k, v):
        if k in d:
            return k, v.value if isinstance(v, BaseTag) else v
        else:
            return k, rd[k].value if isinstance(rd[k], BaseTag) else rd[k]

    def loadWorld(self, io=None):
        returnDict = {}

        if io is None:
            with gzip.open(self.path, 'rb') as io:
                nbtObject = NBTFile(io)
        else:
            nbtObject = NBTFile(io)

        if nbtObject.name != "ClassicWorld":
            raise WorldLoadError(ERRORS["header_mismatch"], "Header mismatch. Maybe the file is broken?")
        if nbtObject["FormatVersion"].value not in self.ACCEPTABLE_LEVEL_VERSIONS:
            raise WorldLoadError(ERRORS["unsupported_level_version"], "Level version unsupported.")

        returnDict.update(walkDictWithRef(nbtObject, self.requiredFields, self._loadRequired, lambda k, v: not isinstance(v, dict)))
        returnDict.update(walkDictWithRef(nbtObject, self.optionalFields, self._loadOptional, lambda k, v: not isinstance(v, dict)))
        self.logger.debug(returnDict)
        return returnDict

    def saveWorld(self, data, io=None):
        returnDict = {}
        returnDict.update(walkDictWithRef(data, self.requiredFields, self._saveRequired, lambda k, v: not isinstance(v, dict)))
        returnDict.update(walkDictWithRef(data, self.optionalFields, self._saveOptional, lambda k, v: not isinstance(v, dict)))

        nbtObject = NBTFile(value=returnDict)
        if io is None:
            with gzip.open(self.path + ".tmp", 'rb') as io:
                nbtObject.save(io, True)
        else:
            nbtObject.save(io, True)

        nbtObject.save()
        shutil.move(self.path + ".tmp", self.path)