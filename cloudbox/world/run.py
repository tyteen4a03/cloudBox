# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from cloudbox.world.factory import WorldServerFactory


def init(serv):
    serv.loadConfig(populate=False)
    # Minecraft part of the Hub
    serv.factories["WorldServerFactory"] = WorldServerFactory(serv)

    # Populate configuration.
    serv.populateConfig()

    # Start up everything.
    # Until Endpoint has reconnection abilities, this is unused
    #TCP4ClientEndpoint(reactor, serv.settings["world"]["main"]["hub-ip"],
    #                   serv.settings["world"]["main"]["hub-port"]).connect(serv.factories["WorldServerFactory"]).addCallback(serv.factories["WorldServerFactory"])

    reactor.connectTCP(serv.factories["WorldServerFactory"].settings["main"]["hub-ip"],
                       serv.factories["WorldServerFactory"].settings["main"]["hub-port"],
                       serv.factories["WorldServerFactory"])
    reactor.run()


def shutdown(serv):
    reactor.stop()