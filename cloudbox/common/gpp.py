# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import importlib
import logging

import msgpack
from twisted.internet.protocol import Factory
from zope.interface import implements

from cloudbox.common.interfaces import IGeneralPacketProcessor


class BaseGeneralPacketProcessor(object):
    """
    GPP Base.
    """
    implements(IGeneralPacketProcessor)

    name = None

    def __init__(self, parent, handlers):
        self.parent = parent
        self.handlers = handlers
        self.handlerInstances = {}
        self.logger = logging.getLogger("cloudbox.gpp.{}".format(self.name))

    @property
    def serverType(self):
        return self.parent.serverType

    def feed(self, data):
        pass

    def parseFirstPacket(self):
        pass

    def packPacket(self, packetID, packetData):
        pass


class MSGPackPacketProcessor(BaseGeneralPacketProcessor):
    """
    A General Packet Processor for MSGPack packets.
    """

    name = "msgpack"

    def __init__(self, parent, handlers):
        """
        Initialization.
        """
        self.unpacker = msgpack.Unpacker()
        self.packer = msgpack.Packer()
        super(MSGPackPacketProcessor, self).__init__(parent, handlers)
        self.requests = {}  # Request ID: callback

    def feed(self, data):
        self.unpacker.feed(data)

    def parseFirstPacket(self):
        """
        Parses the first packet received in the buffer and pass it onto the handler.
        """
        # Try to decode the data
        data = self.unpacker.unpack()
        if not data:
            return  # Try again later
        # Read the handler
        handler = data[0]
        if handler not in self.handlers.keys():
            # TODO Client identifier
            self.logger.error("Client sent unparsable data (%s, %s)", (handler, data[1:].join(" ")))
        if handler not in self.handlerInstances.keys():
            self.initHandlerClass(handler)
        # Pass it on to the handler to handle this request
        self.handlerInstances[handler].handleData(data[1:])

    def packPacket(self, packetID, packetData, callback=None):
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        return self.handlerInstances[packetID].packData(packetData, callback=callback)

    def initHandlerClass(self, handlerID):
        # Grab the class
        handlerEntry = self.handlers[handlerID]
        self.handlerInstances[handlerID] = getattr(importlib.import_module(handlerEntry[0]), handlerEntry[1])(self.parent, self.logger)
        self.handlerInstances[handlerID].packer = self.packer
        self.handlerInstances[handlerID].unpacker = self.unpacker


class MinecraftClassicPacketProcessor(BaseGeneralPacketProcessor):
    """
    A General Packet Processor for Minecraft packets.
    """
    name = "minecraftClassic"

    def __init__(self, parent, handlers):
        super(MinecraftClassicPacketProcessor, self).__init__(parent, handlers)
        # Reference from the protocol - this /may/ cause problems due to lots of GPPs being created at peak hours,
        # but it's fine for now - need to monitor
        self.buffer = ""

    def feed(self, data):
        self.buffer += data

    def parseFirstPacket(self):
        # Examine the first byte, to see what the command is
        packetID = ord(self.buffer[0])
        try:
            packetFormat = self.handlers[packetID]
        except KeyError:
            # Out of range - unknown packet.
            return
        # See if we have all its data
        expectedLength = packetFormat.getExpectedLength()
        if len(self.buffer) - 1 < expectedLength:
            # Nope, wait a bit
            return
        # OK, decode the data
        packetData = list(packetFormat.unpackData(self.buffer[1:]))
        self.buffer = self.buffer[expectedLength + 1:]
        # Pass it on to the handler to handle this request
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        self.handlers[packetID].handleData(packetData)

    def packPacket(self, packetID, packetData, withoutHeader=False):
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        header = "" if withoutHeader else chr(packetID)
        packed = self.handlers[packetID].packData(packetData)
        return header + packed

    def initHandlerClass(self, handlerID):
        # Grab the class
        handlerEntry = self.handlers[handlerID]
        self.handlerInstances[handlerID] = getattr(importlib.import_module(handlerEntry[0]), handlerEntry[1])(self.parent, self.logger)