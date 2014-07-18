# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import nbt.nbt as nbt
from zope.interface import implements

from cloudbox.common.constants.common import *
from cloudbox.common.constants.world import *
from cloudbox.world.exceptions import WorldLoadError
from cloudbox.world.interfaces import IWorldFormat


class ClassicWorldWorldFormat(object):
    implements(IWorldFormat)

    name = "ClassicWorld Format"
    supportsLoading = True
    supportsSaving = True

    worldStorageType = "file"
    fileExtensions = ["cw"]

    CURRENT_LEVEL_VERSION = 0
    ACCEPTABLE_LEVEL_VERSIONS = [0]

    requiredFields = ["Name", "UUID", "X", "Y", "Z", "Spawn", "BlockArray" "Metadata"]
    optionalFields = ["CreatedBy", "MapGeneratorUsed", "TimeCreated", "LastAccessed", "LastModified"]

    def __init__(self, path):
        self.path = path

    def loadWorld(self, io=None):
        returnDict = {}
        if io is None:
            nbtObject = nbt.NBTFile(fileobj=open(self.path, "r"))
        else:
            nbtObject = nbt.NBTFile(fileobj=io)

        if nbtObject.name != "ClassicWorld":
            raise WorldLoadError(ERRORS["header_mismatch"], "Header mismatch. Maybe the file is broken?")
        if nbtObject["FormatVersion"] not in ClassicWorldWorldFormat.ACCEPTABLE_LEVEL_VERSIONS:
            raise WorldLoadError(ERRORS["unsupported_level_version"], "Level version unsupported.")
        missing = []
        for r in self.requiredFields:
            if not nbtObject[r]:
                missing.append(r)
            else:
                returnDict[r] = nbtObject[r]
        if missing:
            raise WorldLoadError(ERRORS["required_fields_missing"], "Required field(s) {} missing.".format(", ".join(missing)))
        for r in self.optionalFields:
            if nbtObject[r]:
                returnDict[r] = nbtObject[r]
            else:
                returnDict[r] = None
        return returnDict

    def saveWorld(self, data):
        pass