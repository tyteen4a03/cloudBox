# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from pubsub import pub
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ClientEndpoint

from cloudbox.world.factory import WorldServerFactory


def init(serv):
    serv.loadConfig(populate=False)
    # Minecraft part of the Hub
    wsFactory = serv.factories["WorldServerFactory"] = WorldServerFactory(serv)

    # Populate configuration.
    serv.populateConfig()

    # Load up the database.
    serv.loadDatabase()

    # Start up everything.
    # Until Endpoint has reconnection abilities, this is unused
    #TCP4ClientEndpoint(reactor, serv.settings["world"]["main"]["hub-ip"],
    #                   serv.settings["world"]["main"]["hub-port"]).connect(serv.factories["WorldServerFactory"]).addCallback(serv.factories["WorldServerFactory"])

    def afterLoadedPreloadedWorlds():
        reactor.connectTCP(wsFactory.settings["main"]["hub-ip"], wsFactory.settings["main"]["hub-port"], wsFactory)

    def afterLoadedSelfID():
        serv.factories["WorldServerFactory"].loadPreloadedWorlds().addCallback(afterLoadedPreloadedWorlds)

    def afterDBAPIReady():
        # Get our ID
        wsFactory.loadID().addCallback(afterLoadedSelfID)

    pub.subscribe(afterDBAPIReady, "cloudbox.common.service.databaseAPIReady")

    reactor.run()

def shutdown(serv):
    serv.factories["WorldServerFactory"].quit()
    reactor.stop()