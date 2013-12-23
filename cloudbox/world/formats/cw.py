# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import cStringIO

import nbt
from twisted.python.failure import Failure
from zope.interface import implements

from cloudbox.common.constants.world import *
from cloudbox.common.exceptions import makeFailure
from cloudbox.world.interfaces import IWorldFormat
from cloudbox.world.worlds.classic import ClassicWorld


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

    @staticmethod
    def loadWorld(filepath):
        returnDict = {}
        with open(filepath, "r") as fo:
            _nbtFile = fo.read()
        nbtObject = nbt.NBTFile(cStringIO.StringIO(_nbtFile))
        if nbtObject.name != "ClassicWorld":
            return makeFailure(ERROR_HEADER_MISMATCH, "Header mismatch. Maybe the file is broken?")
        if nbtObject["FormatVersion"] not in ClassicWorldWorldFormat.ACCEPTABLE_LEVEL_VERSIONS:
            return makeFailure(ERROR_UNSUPPORTED_LEVEL_VERSION, "Level version unsupported.")
        for r in ClassicWorldWorldFormat.requiredFields:
            if not nbtObject[r]:
                return makeFailure(ERROR_REQUIRED_FIELDS_MISSING, "Required field {} missing.".format(r))
            returnDict[r] = nbtObject[r]
        for r in ClassicWorldWorldFormat.optionalFields:
            if nbtObject[r]:
                returnDict[r] = nbtObject[r]
            else:
                returnDict[r] = None
        return returnDict

    @staticmethod
    def saveWorld(filepath, data):
        pass