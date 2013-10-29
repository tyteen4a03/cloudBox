# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import urllib

from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.internet.task import LoopingCall
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implements

from cloudbox.common.logger import Logger
from cloudbox.common.constants.common import VERSION


class _StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class HeartbeatService(object):
    """
    I send heartbeats to Minecraft.net/ClassiCube every so often.
    """

    def __init__(self, parentService, hburl):
        self.parentService = parentService
        self.hburl = hburl
        self.logger = Logger()
        self.agent = Agent(reactor)
        self.loop = None
        self.running = False

    def start(self):
        self.loop = LoopingCall(self.sendHeartbeat).start(30)  # TODO Dynamic timeframe
        self.logger.info("HeartbeatService to %s started." % self.hburl)
        self.running = True

    def stop(self):
        self.loop.stop()
        self.logger.info("HeartbeatService to %s stopped." % self.hburl)
        self.running = False

    def getMCFactoryInstance(self):
        return self.parentService.factories["MinecraftHubServerFactory"]

    @property
    def hbdata(self):
        mcFactory = self.getMCFactoryInstance()
        return urllib.urlencode({
            "port": mcFactory.settings["main"]["ports"]["clients"],
            "users": len(mcFactory.clients),
            "max": mcFactory.settings["main"]["max-clients"],
            "name": mcFactory.settings["main"]["name"],
            "public": mcFactory.settings["main"]["public"],
            "version": 7,
            "salt": mcFactory.settings["main"]["salt"],
        })

    def sendHeartbeat(self):
        """
        Sends Heartbeat.
        """
        self.agent.request(
            'POST',
            self.hburl,
            Headers({'User-Agent': ['cloudBox %s' % VERSION],
                     'Content-Type': ['application/x-www-form-urlencoded']}),
            _StringProducer(self.hbdata)
        ).addCallbacks(self.heartbeatSentCallback).addErrback(self.heartbeatFailedCallback)

    def heartbeatSentCallback(self, thing):
        self.logger.info("Heartbeat successfully sent to %s." % self.hburl)

    def heartbeatFailedCallback(self, failure):
        self.logger.warn("Heartbeat failed to send. Error: %s" % str(failure))
