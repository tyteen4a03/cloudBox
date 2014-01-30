# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import Queue

from twisted.internet.defer import Deferred
from twisted.internet.task import LoopingCall

from cloudbox.common.constants.common import *
from cloudbox.common.constants.handlers import *
from cloudbox.common.loops import LoopRegistry


class CloudBoxFactoryMixin(object):
    """
    A mixin class, providing common functions any cloudBox factories can expect.
    """

    parentService = None

    @property
    def serverName(self):
        return self.parentService.settings[SERVER_TYPES_ABBRV_INV[self.parentService.serverType]]["main"]["server-name"]

    @property
    def serverType(self):
        return self.parentService.serverType

    @property
    def db(self):
        return self.parentService.db

    def getFactory(self, factoryName):
        return self.parentService.factories[factoryName]


class CloudBoxProtocolMixin(object):
    """
    A mixin class, providing common functions any cloudBox protocols can expect.
    """

    loops = LoopRegistry()

    @property
    def serverName(self):
        return self.factory.serverName

    @property
    def serverType(self):
        return self.factory.serverType

    @property
    def db(self):
        return self.factory.db

    def sendPacket(self, packetID, packetData={}):
        self.transport.write(self.gpp.packPacket(packetID, packetData))

    def getRequestsPerTick(self, entry):
        return self.factory.getRequestsPerTick(entry)

    def getTickInterval(self, entry=""):
        return self.factory.getTickInterval(entry)

    def sendHandshake(self):
        self.sendPacket(TYPE_HANDSHAKE)

    def sendError(self, error, errorID=ERRORS["unknown"]):
        self.sendDisconnect(DISCONNECT_ERROR, errorID, error)

    def sendServerShutdown(self, reason=""):
        self.sendDisconnect(DISCONNECT_SHUTDOWN, reason)

    def sendDisconnect(self, disconnectType=DISCONNECT_GENERIC, errorID=ERRORS["unknown"], message=""):
        self.sendPacket(TYPE_DISCONNECT, {"disconnectType": disconnectType, "errorID": errorID, "message": message})


class TickMixin(object):
    """
    Base class for other tick mixins.
    """

    def getRequestsPerTick(self, entry):
        return self.parentService.settings["common"]["advanced"]["requests-per-tick"][SERVER_TYPES_ABBRV_INV[self.serverType] + "-" + entry]

    def getTickInterval(self, entry=""):
        return self.parentService.settings["common"]["advanced"]["tick-interval"][SERVER_TYPES_ABBRV_INV[self.serverType]]


class TaskTickMixin(TickMixin):
    """
    A mixin for classes that wishes to use a task-based event loop. Expects a CloudBoxFactory/ProtocolMixin.
    """

    tasks = Queue.PriorityQueue()
    taskHandlers = []
    TASK_LIMIT_NAME = "tasks"  # Hack

    def addTask(self, taskID, taskData={}, priority=5):
        d = Deferred()
        self.tasks.put_nowait((
            priority,
            taskID,
            taskData,
            d
        ))
        return d

    def taskTick(self):
        def _tick():
            nextItem = self.tasks.get_nowait()  # (priority, (taskID, taskData, deferred))
            # Pass on for the task handler to handle the task
            func = getattr(self, self.taskHandlers[nextItem[1][0]])
            func(nextItem[1][1], nextItem[1][2])  # The handler function decides when to d.callback()

        limit = self.getRequestsPerTick(self.TASK_LIMIT_NAME)
        if limit == -1:
            while not self.tasks.empty():
                _tick()
        else:
            for i in range(0, limit):
                try:
                    _tick()
                except Queue.Empty:
                    break

    def setUpTaskLoop(self):
        return LoopingCall(self.taskTick)


class PacketTickMixin(TickMixin):
    """
    A mixin for packet sending. Expects a CloudBoxProtocolMixin.
    """
    packetsOut = Queue.PriorityQueue()

    def sendPacket(self, packetID, packetData={}, priority=5):
        d = Deferred()
        self.packetsOut.put_nowait((
            priority,
            self.gpp.packPacket(packetID, packetData),
            d
        ))
        return d

    def packetTick(self):
        def _tick():
            nextItem = self.packetsOut.get_nowait()  # (priority, (prepacked packet, callback))
            self.transport.write(nextItem[1][0])
            if isinstance(nextItem[1][1], Deferred):
                nextItem[1][1].callback()

        limit = self.getRequestsPerTick("outgoing-minecraft")
        if limit == -1:
            while not self.packetsOut.empty():
                _tick()
        else:
            for i in range(0, limit):
                try:
                    _tick()
                except Queue.Empty:
                    break

    def setUpPacketLoop(self):
        return LoopingCall(self.packetTick)