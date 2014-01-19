# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.minecraft.handlers.classic import BaseMinecraftPacketHandler


class ExtInfoPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for handling extension information.
    """

    @classmethod
    def handleData(cls, data):
        pass

    @classmethod
    def packData(cls, data):
        pass

class ExtEntryPacketHandler(BaseMinecraftPacketHandler):
    """
    A Handler class for handling extension entries.
    """

    @classmethod
    def handleData(cls, data):
        pass

    @classmethod
    def packData(cls, data):
        pass
