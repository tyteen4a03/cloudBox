# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import importlib
import logging
import Queue

import msgpack
from twisted.internet.defer import Deferred
from twisted.internet.task import LoopingCall
from zope.interface import implements

from cloudbox.common.interfaces import IGeneralPacketProcessor


class BaseGeneralPacketProcessor(object):
    """
    GPP Base.
    """
    implements(IGeneralPacketProcessor)

    name = None
    packetsOut = Queue.PriorityQueue()

    def __init__(self, parent, handlers, transport):
        self.parent = parent
        self.handlers = handlers
        self.transport = transport
        self.requests = []
        self.handlerInstances = {}
        self.logger = logging.getLogger("cloudbox.gpp.{}".format(self.name))

    @property
    def serverName(self):
        return self.parent.serverName

    @property
    def serverType(self):
        return self.parent.serverType

    def feed(self, data):
        pass

    def parseFirstPacket(self):
        pass

    def packPacket(self, packetID, packetData, requestID=None):
        pass

    def sendPacket(self, packetID, packetData={}, requestID=None, priority=5):
        d = Deferred()
        self.requests.append(d)
        if not requestID:
            requestID = len(self.requests) - 1
        self.packetsOut.put_nowait((
            priority,
            (self.packPacket(packetID, packetData, requestID), d)
        ))
        self.logger.info("Packet added to queue: {} {}".format(packetID, packetData))
        return d

    def _sendPacket(self, packet):
        self.transport.write(packet)

    def initHandlerClass(self, handlerID):
        # Grab the class
        handlerEntry = self.handlers[handlerID]
        self.handlerInstances[handlerID] = getattr(importlib.import_module(handlerEntry[0]), handlerEntry[1])(self.parent, self.logger, self.transport)

    def packetTick(self):
        if self.packetsOut.empty():
            # Don't bother
            return

        def _tick():
            nextItem = self.packetsOut.get_nowait()  # (priority, (prepacked packet, callback))
            self._sendPacket(nextItem[1][0])

        limit = self.parent.getRequestsPerTick(self.parent.PACKET_LIMIT_NAME)
        if limit == -1:
            while not self.packetsOut.empty():
                _tick()
        else:
            for i in range(0, limit):
                try:
                    _tick()
                except Queue.Empty:
                    break

    @property
    def packetLoop(self):
        return LoopingCall(self.packetTick)


class MSGPackPacketProcessor(BaseGeneralPacketProcessor):
    """
    A General Packet Processor for MSGPack packets.
    """

    name = "msgpack"

    def __init__(self, parent, handlers, transport):
        """
        Initialization.
        """
        self.unpacker = msgpack.Unpacker()
        self.packer = msgpack.Packer()
        super(MSGPackPacketProcessor, self).__init__(parent, handlers, transport)
        self.requests = []  # Request ID: callback

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
            self.logger.error("Client sent unparsable data (%s, %s)", (handler, repr(data[2])))
        if handler not in self.handlerInstances.keys():
            self.initHandlerClass(handler)
        requestID = data[1] if data[1] > 0 else None  # requestID 0 = not expecting a response

        # Pass it on to the handler to handle this request
        self.handlerInstances[handler].handleData(data[2], requestID)

    def packPacket(self, packetID, packetData, requestID=None):
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        data = self.handlerInstances[packetID].packData(packetData)
        return self.packer.pack([packetID, requestID, data])

    def initHandlerClass(self, handlerID):
        super(MSGPackPacketProcessor, self).initHandlerClass(handlerID)
        self.handlerInstances[handlerID].packer = self.packer
        self.handlerInstances[handlerID].unpacker = self.unpacker


class MinecraftClassicPacketProcessor(BaseGeneralPacketProcessor):
    """
    A General Packet Processor for Minecraft packets.
    """
    name = "minecraftClassic"

    def __init__(self, parent, handlers, transport):
        super(MinecraftClassicPacketProcessor, self).__init__(parent, handlers, transport)
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
        # Make me an instance
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        handler = self.handlerInstances[packetID]
        # See if we have all its data
        if len(self.buffer) - 1 < handler.expectedLength:
            # Nope, wait a bit
            return
        # OK, decode the data
        packetData = list(handler.unpackData(self.buffer[1:]))
        self.buffer = self.buffer[handler.expectedLength + 1:]
        # Pass it on to the handler to handle this request
        handler.handleData(packetData, 0)

    def sendPacket(self, packetID, packetData={}, requestID=None, priority=5):
        d = Deferred()
        self.packetsOut.put_nowait((
            priority,
            (self.packPacket(packetID, packetData), d)
        ))
        self.logger.info("Packet added to queue: {}".format(packetID))
        return d

    def packPacket(self, packetID, packetData, withoutHeader=False):
        if packetID not in self.handlerInstances.keys():
            self.initHandlerClass(packetID)
        header = "" if withoutHeader else chr(packetID)
        packed = self.handlerInstances[packetID].packData(packetData)
        return header + packed