# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from Queue import Queue

from twisted.enterprise.adbapi import ConnectionPool
from twisted.internet.protocol import ServerFactory
from twisted.python.failure import Failure

from cloudbox.common.constants.handlers import *
from cloudbox.common.logger import Logger
from cloudbox.common.mixins import CloudBoxFactoryMixin
from cloudbox.database.server.protocol import DatabaseServerProtocol


class DatabaseServerFactory(ServerFactory, CloudBoxFactoryMixin):
    """I am a database server that takes requests from nodes."""

    protocol = DatabaseServerProtocol

    def __init__(self, parentService):
        self.parentService = parentService
        self.logger = Logger()
        self.requests = []  # Central requests list, used to keep track of requests
        self.handlers = self.buildHandlers()
        self.dbapi = None
        self.ready = False

    def buildHandlers(self):
        h = dict(HANDLERS_CLIENT_BASIC.items() + HANDLERS_DATABASE_SERVER.items())
        return h

    def startFactory(self):
        connArgs, connKwargs = self.buildConnectionParameters()
        self.dbapi = ConnectionPool(self.settings["main"]["driver"], *connArgs, **connKwargs)
        # Perform basic validation check
        self.dbapi.runQuery("SELECT name, value FROM cb_global_metadata").addBoth(self.checkTablesCallabck)

    def checkTablesCallabck(self, res):
        if isinstance(res, Failure):
            self.logger.critical("Database validation check failed:")
            self.logger.critical(res.getTraceback())
            self.parentService.stop()
        else:
            self.logger.debug(str(res))
            self.ready = True
            self.logger.debug("Database API ready.")

    def buildConnectionParameters(self):
        connArgs = []
        connKwargs = dict()
        try:
            dbModule = __import__(("%s" % self.settings["main"]["driver"]))
        except ImportError:
            self.logger.critical("Database module {dbModule} not found, stopping.".format(dbModule=dbModule))
            self.parentService.stop()
        if self.settings["main"]["driver"] == "sqlite3":
            connKwargs["database"] = self.settings["driver"]["file"]
        # TODO Implement
        elif self.settings["main"]["driver"] == "txmysql":
            connKwargs = {}
        elif self.settings["main"]["driver"] == "txpostgres":
            connKwargs = {}
        elif self.settings["main"]["driver"] == "mysql-python":
            connKwargs = {}
        elif self.settings["main"]["driver"] == "psycopg2":
            connKwargs = {}
        return tuple(connArgs), connKwargs