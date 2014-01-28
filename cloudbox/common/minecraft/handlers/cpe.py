# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants.cpe import *
from cloudbox.common.minecraft.handlers.classic import BaseMinecraftPacketHandler


class ExtInfoPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for handling extension information.
    """

    packetID = TYPE_EXTINFO

    def handleData(self, packetData):
        pass

    def packData(self, packetData):
        pass

class ExtEntryPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for handling extension entries.
    """

    packetID = TYPE_EXTENTRY

    def handleData(self, packetData):
        pass

    def packData(self, packetData):
        pass
