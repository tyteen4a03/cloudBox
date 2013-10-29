# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.task import LoopingCall
from zope.interface import implements

from cloudbox.common.interfaces import ILoopRegistry

class LoopRegistry(object):
    """
    I am the loop Registry. I keep all LoopingCalls together, allowing plugin authors
    to easily keep track of them.
    I can be used from anywhere.
    """

    implements(ILoopRegistry)
    loops = {}

    def registerLoop(self, name, obj):
        if not isinstance(obj, LoopingCall):
            raise TypeError
        self.loops[name] = obj
        return self.loops[name]  # For laziness

    def unregisterLoop(self, name):
        self.loops[name].stop()
        del self.loops[name]

    def __iter__(self):
        for loop in self.loops:
            yield loop
