# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from pubsub import pub
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from cloudbox.hub.heartbeat import HeartbeatService
from cloudbox.hub.minecraft.factory import MinecraftHubServerFactory
from cloudbox.hub.world.factory import WorldServerCommServerFactory


def init(serv):
    # Populate configuration.
    serv.loadConfig(populate=False)

    # Minecraft part of the Hub
    serv.factories["MinecraftHubServerFactory"] = MinecraftHubServerFactory(serv)
    # WorldServer part of the Hub
    serv.factories["WorldServerCommServerFactory"] = WorldServerCommServerFactory(serv)

    serv.populateConfig()

    # Load up the database.
    serv.loadDatabase()

    # Start up everything.
    def afterDBAPIReady():
        TCP4ServerEndpoint(reactor, serv.settings["hub"]["main"]["ports"]["clients"])\
            .listen(serv.factories["MinecraftHubServerFactory"])
        TCP4ServerEndpoint(reactor, serv.settings["hub"]["main"]["ports"]["worldservers"])\
            .listen(serv.factories["WorldServerCommServerFactory"])
        logging.getLogger("cloudbox.hub").info("Listeners started successfully - now accepting incoming connections.")
        # Heartbeat Service
        if serv.settings["hub"]["heartbeat"]["send-heartbeat"]:
            if serv.settings["hub"]["heartbeat"]["minecraft-heartbeat"]:
                serv.factories["HeartbeatService-Minecraft"] = HeartbeatService(serv, "Minecraft",
                    "http://minecraft.net/heartbeat.jsp").start()
            if serv.settings["hub"]["heartbeat"]["classicube-heartbeat"]:
                serv.factories["HeartbeatService-ClassiCube"] = HeartbeatService(serv, "ClassiCube",
                    "http://www.classicube.net/server/heartbeat").start()
            logging.getLogger("cloudbox.hub").info("HeartbeatServices started successfully.")

    pub.subscribe(afterDBAPIReady, "cloudbox.common.service.databaseAPIReady")

    reactor.run()


def shutdown(serv):
    reactor.stop()