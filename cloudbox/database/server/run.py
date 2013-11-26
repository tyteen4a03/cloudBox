# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from cloudbox.database.server.factory import DatabaseServerFactory


# In the future, this function will be able to run in either client mode or server mode. Right now only server mode is
# implemented, so the check is skipped.
def init(serv):
    serv.factories["DatabaseServerFactory"] = DatabaseServerFactory(serv)

    serv.loadConfig()

    # Start up everything.
    TCP4ServerEndpoint(reactor, serv.settings["database"]["main"]["port"])\
        .listen(serv.factories["DatabaseServerFactory"])

    reactor.run()


def shutdown(serv):
    # Stop incoming connections
    serv.factories["DatabaseServerFactory"].ready = False

    def checkQueriesList():
        if not serv.factories["DatabaseServerFactory"].requests:  # Requests are all sent out, hooray
            reactor.stop()
        reactor.callLater(0.1, checkQueriesList)
    checkQueriesList()