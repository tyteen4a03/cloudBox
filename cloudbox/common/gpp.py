# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import importlib

import msgpack
from zope.interface import implements

from cloudbox.common.interfaces import IGeneralPacketProcessor
from cloudbox.common.logger import Logger


class BaseGeneralPacketProcessor(object):
    """
    GPP Base.
    """
    implements(IGeneralPacketProcessor)

    def __init__(self, parent, handlers, serverType=None):
        self.parent = parent
        self.handlers = handlers
        self.handlersClassRefs = {}
        self.logger = Logger()
        self.baseVariables = {}
        if serverType:
            self.serverType = serverType
        else:
            self.serverType = self.parent.getServerType()
        self.baseVariables = {
            "serverType": self.serverType,
            "parent": self.parent,
            "logger": self.logger
        }

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

    def __init__(self, parent, handlers):
        """
        Initialization.
        """
        self.unpacker = msgpack.Unpacker()
        self.packer = msgpack.Packer()
        super(MSGPackPacketProcessor, self).__init__(parent, handlers)
        self.baseVariables["packer"] = self.packer
        self.baseVariables["unpacker"] = self.unpacker

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
        self.logger.info(str(data))
        # Read the handler
        handler = data[0]
        if handler not in self.handlers.keys():
            # TODO Client identifier
            self.logger.error("Client sent unparsable data (%s, %s)", (handler, data[1:].join(" ")))
        # TODO Factorize?
        if handler not in self.handlersClassRefs.keys():
            self.initHandlerClass(handler)
        # Pass it on to the handler to handle this request
        # TODO Unify this
        dataDict = self.baseVariables
        dataDict["packetData"] = data[1:]  # Don't pass the packet ID
        self.handlersClassRefs[handler].handleData(dataDict)

    def packPacket(self, packetID, packetData):
        if packetID not in self.handlersClassRefs.keys():
            self.initHandlerClass(packetID)
        return self.handlersClassRefs[packetID].packData(dict(packetData, **self.baseVariables))

    def initHandlerClass(self, handlerID):
        # Grab the class
        handlerEntry = self.handlers[handlerID]
        cls = getattr(importlib.import_module(handlerEntry[0]), handlerEntry[1])
        self.handlersClassRefs[handlerID] = cls


class MinecraftClassicPacketProcessor(BaseGeneralPacketProcessor):
    """
    A General Packet Processor for Minecraft packets.
    """
    implements(IGeneralPacketProcessor)

    def __init__(self, parent, handlers):
        super(MinecraftClassicPacketProcessor, self).__init__(parent, handlers)
        # Reference from the protocol - this /may/ cause problems due to lots of GPPs being created at peak hours,
        # but it's fine for now - need to monitor
        self.buffer = ""

    def feed(self, data):
        self.buffer += data

    def parseFirstPacket(self):
        # Examine the first byte, to see what the command is
        packetType = ord(self.buffer[0])
        try:
            packetFormat = self.handlers[packetType]
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
        # TODO Unify that
        self.handlers[packetType].handleData(dict({
            "parent": self.parent,
            "packetData": packetData
        }, **self.baseVariables))
