# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import array
import importlib

from twisted.internet.threads import deferToThread
from zope.interface import implements

from cloudbox.common.constants.cpe import *
from cloudbox.common.constants.world import SUPPORTED_WORLD_LOADERS
from cloudbox.world.interfaces import IWorld


class ClassicWorld(object):
    """
    I am a Minecraft Classic world.
    """
    implements(IWorld)

    def __init__(self, factory, **worldParams):
        self.factory = factory
        self.worldID = None
        self.worldReady = False
        self.worldParams = worldParams
        self.format = None
        self.name = None
        self.x = None
        self.y = None
        self.z = None
        self.uuid = None
        self.spawn = (None, None, None, None, None)  # x, y, z, h, p
        self.additionalData = {}
        self.blockData = bytearray()
        self.metadata = {}
        self.fullMetadata = {}
        self.physics = None  # Physics engine here

    def loadWorld(self):
        return deferToThread(self._loadWorld)

    def _loadWorld(self):
        data = self.format.loadWorld()
        # Unpack data
        self.name = data["Name"]
        self.x, self.y, self.z = data["X"], data["Z"], data["Y"]  # Blame OpenGL
        self.uuid = data["UUID"]
        self.spawn = (data["Spawn"]["X"], data["Spawn"]["Z"], data["Spawn"]["Y"],  # Blame OpenGL
                      data["Spawn"]["H"], data["Spawn"]["P"])
        self.additionalData = {
            "CreatedBy": data["CreatedBy"],
            "MapGenerator": data["MapGenerator"],
            "TimeCreated": data["TimeCreated"],
            "LastAccessed": data["LastAccessed"],
            "LastModified": data["LastModified"],
        }
        self.metadata = data["Metadata"]["cloudBox"]
        self.fullMetadata = data["Metadata"]
        self.worldReady = True

    def saveWorld(self):
        return deferToThread(self._saveWorld)

    def _saveWorld(self):
        # Prepare data
        data = {
            "Name": self.name,
            "UUID": self.uuid,
            "X": self.x,
            "Y": self.z,
            "Z": self.y,
            "CreatedBy": self.additionalData["CreatedBy"],
            "MapGenerator": self.additionalData["MapGenerator"],
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
        }
        self.format.saveWorld(data)

    @staticmethod
    def filterCPEBlocks(blockArray, fallbackArray=CPE_EXTENSIONS["CustomBlocks"]["Fallback"]):
        for supportLevel, slBlocks in fallbackArray:
            for block, fallback in slBlocks:
                blockArray.replace(block, fallback)
        return blockArray