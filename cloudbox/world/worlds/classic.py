# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import array
import importlib

from twisted.internet.threads import deferToThread
from zope.interface import implements

from cloudbox.common.constants.cpe import *
from cloudbox.common.constants.world import SUPPORTED_LEVEL_FORMATS
from cloudbox.world.interfaces import IWorld


class ClassicWorld(object):
    """
    I am a Minecraft Classic world.
    """
    implements(IWorld)

    def __init__(self, factory, **worldParams):
        self.factory = factory
        self.worldReady = False
        self.worldParams = worldParams
        self.name = None
        self.x = None
        self.y = None
        self.z = None
        self.uuid = None
        self.spawn = (None, None, None, None, None)  # x, y, z, h, p
        self.additionalData = {}
        self.blockData = bytearray()
        self.metadata = {}
        self.CPEMetadata = {}
        self.blockMetadata = {}
        self.physics = None  # Physics engine here

    def loadWorld(self):
        # TODO File IO needs own process?
        deferToThread(self._loadWorld)

    def _loadWorld(self):
        # Get the handler
        cls = getattr(importlib.import_module(SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][0]]),
                      SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][1]])
        data = cls.loadWorld(self.worldParams["filePath"])
        # Unpack data
        self.name = data["Name"]
        self.x, self.y, self.z = data["X"], data["Z"], data["Y"]  # Blame Notch
        self.uuid = data["UUID"]
        self.spawn = (data["Spawn"]["X"], data["Spawn"]["Z"], data["Spawn"]["Y"],  # Blame Notch
                      data["Spawn"]["H"], data["Spawn"]["P"])
        self.additionalData = {
            "CreatedBy": data["CreatedBy"],
            "MapGenerator": data["MapGenerator"],
            "TimeCreated": data["TimeCreated"],
            "LastAccessed": data["LastAccessed"],
            "LastModified": data["LastModified"],
        }
        self.metadata = data["Metadata"]["cloudBox"]
        self.blockMetadata = self.metadata["_BlockMetadata"]
        self.worldReady = True

    def saveWorld(self):
        deferToThread(self._saveWorld)

    def _saveWorld(self):
        # Get the handler
        cls = getattr(importlib.import_module(SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][0]]),
                      SUPPORTED_LEVEL_FORMATS[self.worldParams["worldType"][1]])
        # Prepare data
        data = {
            "Name": self.name,
            "UUID": self.uuid,
            "X": self.x,
            "Y": self.z,
            "Z": self.y,
            "CreatedBy": self.additionalData["CreatedBy"],
            "MapGeneratorUsed": self.additionalData["MapGeneratorUsed"],
            "TimeCreated": self.additionalData["TimeCreated"],
            "LastAccessed": self.additionalData["LastAccessed"],
            "LastModified": self.additionalData["LastModified"],
            "Spawn": {
                "X": self.spawn[0],
                "Y": self.spawn[2],
                "Z": self.spawn[1],
                "H": self.spawn[3],
                "P": self.spawn[4]
            },
            "BlockArray": self.blockData,
            "Metadata": {
                "cloudBox": self.metadata
            },
            "BlockMetadata": {
                "cloudBox": self.blockMetadata
            },
        }
        cls.saveWorld(self.worldParams["filePath"], data)

    @staticmethod
    def filterCPEBlocks(blockArray, fallbackArray=CPE_EXTENSIONS["CustomBlocks"]["Fallback"]):
        for supportLevel, slBlocks in fallbackArray:
            for block, fallback in slBlocks:
                blockArray.replace(block, fallback)
        return blockArray