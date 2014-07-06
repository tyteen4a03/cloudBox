# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from StringIO import StringIO
import unittest

from cloudbox.common.gpp import MSGPackPacketProcessor
from cloudbox.common.handlers import BasePacketHandler


class TestOnePacketHandler(BasePacketHandler):
    def handleData(self, packetData, requestID):
        self.parent.assertEqual(packetData, self.parent.testDataOne)

    def packData(self, packetData):
        return self.parent.testDataOne


class TestMsgPackGPP(unittest.TestCase):

    def setUp(self):
        self.handlers = {
            0x01: ("cloudbox.tests.test_gpp", "TestOnePacketHandler"),
            0x02: ("cloudbox.tests.test_gpp", "TestTwoPacketHandler")
        }
        self.testDataOne = ["foo", "bar", 123]
        self.out = StringIO()  # Output buffer
        self.gpp = MSGPackPacketProcessor(self, self.handlers, self.out)

if __name__ == '__main__':
    unittest.main()