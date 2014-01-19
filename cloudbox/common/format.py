# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import struct

from cloudbox.common.util import packString
from cloudbox.common.constants.common import FORMAT_LENGTHS


class Format(object):
    """
    Packet format used by Minecraft.
    """

    def __init__(self, format):
        self.format = format

    def __len__(self):
        length = 0
        for char in self.format:
            length += FORMAT_LENGTHS[char]
        return length

    def decode(self, data):
        for char in self.format:
            if char == "b":
                print data
                yield struct.unpack(">B", data[0])[0]
            elif char == "a":
                yield data[:1024]
            elif char == "s":
                yield data[:64].strip()
            elif char == "h":
                yield struct.unpack(">h", data[:2])[0]
            elif char == "i":
                yield struct.unpack(">i", data[:4])[0]
            data = data[FORMAT_LENGTHS[char]:]

    def encode(self, *args):
        assert len(self.format) == len(args)
        data = ""
        for char, arg in zip(self.format, args):
            if char == "a":  # Array, 1024 long
                data += packString(arg[:1024], length=1024, packWith="\0")
            elif char == "s":  # String, 64 long
                data += packString(arg[:64])
            elif char == "h":  # Short
                data += struct.pack(">h", arg)
            elif char == "i":  # Integer
                data += struct.pack(">i", arg)
            elif char == "b":  # Byte
                if isinstance(arg, int):
                    data += chr(arg)
                elif isinstance(arg, str):
                    data += arg
                else:
                    raise ValueError("Invalid value for byte: %r" % arg)
        return data