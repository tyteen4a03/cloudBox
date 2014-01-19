# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

from tornado.httpserver import HTTPServer
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor

from cloudbox.web.application import WebServerApplication


def init(serv):
    TwistedIOLoop().install()

    # TODO Hack
    for l in ["tornado.application", "tornado.general", "tornado.access"]:
        l = logging.getLogger(l)

    serv.loadConfig(populate=False)
    serv.factories["WebServerApplication"] = WebServerApplication(serv)
    serv.populateConfig()

    # TODO Hack
    for l in ["tornado.application", "tornado.general", "tornado.access"]:
        logging.getLogger(l).addHandler(logging.StreamHandler())
    serv.factories["WebHTTPServer"] = HTTPServer(serv.factories["WebServerApplication"])
    serv.factories["WebHTTPServer"].listen(serv.settings["web"]["main"]["port"])

    reactor.run()


def shutdown(serv):
    pass