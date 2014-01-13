# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from tornado.httpserver import HTTPServer
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor

from cloudbox.web.application import WebServerApplication


def init(serv):
    TwistedIOLoop().install()

    serv.loadConfig(populate=False)
    serv.factories["WebServerApplication"] = WebServerApplication(serv)
    serv.populateConfig()
    serv.factories["WebHTTPServer"] = HTTPServer(serv.factories["WebServerApplication"])
    serv.factories["WebHTTPServer"].listen(serv.settings["web"]["main"]["port"])

    reactor.run()


def shutdown(serv):
    pass