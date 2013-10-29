# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from cloudbox.world.factory import WorldServerFactory


def init(serv):
    # Minecraft part of the Hub
    serv.factories["WorldServerFactory"] = WorldServerFactory(serv)

    # Populate configuration.
    serv.loadConfig()

    # Start up everything.
    TCP4ClientEndpoint(reactor, serv.settings["world"]["main"]["hub-ip"],
                       serv.settings["world"]["main"]["hub-port"]).connect(serv.factories["WorldServerFactory"])

    reactor.run()


def stop(serv):
    reactor.stop()