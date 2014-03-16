# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging

# YAML
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase
from twisted.enterprise.adbapi import ConnectionPool
from twisted.python.failure import Failure

from cloudbox.common.constants.common import *
from cloudbox.common.database import checkForFailure
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.models import databaseProxy
from cloudbox.common.models.servers import GlobalMetadata


class CloudBoxService(object):
    """
    The central hub of all services.
    """

    def __init__(self, whoami):
        """
        Initializes the service.
        Whoami contains the server identifier.
        """
        self.logger = logging.getLogger("cloudbox")
        self.serverType = SERVER_TYPES[whoami]
        # Make our loop registry
        self.loops = LoopRegistry()
        self.factories = {}
        self.settings = {}
        self.db = None

    # TODO Factorize below methods

    def loadConfig(self, populate=True, reload=False):
        """
        Loads the configuration file, depending on the SERVER_TYPE of the server.
        Specify reload to make the function reload the configuration. Note that by specifying reload, the function
        assumes that the related factories exist.
        """
        with open("config/common.yaml", "r") as f:
            s = f.read()
        self.settings["common"] = yaml.load(s, Loader)
        if self.serverType == SERVER_TYPES["HubServer"]:
            with open("config/hub.yaml", "r") as f:
                s = f.read()
            self.settings["hub"] = yaml.load(s, Loader)
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            with open("config/world.yaml", "r") as f:
                s = f.read()
            self.settings["world"] = yaml.load(s, Loader)
        elif self.serverType == SERVER_TYPES["WebServer"]:
            with open("config/web.yaml", "r") as f:
                s = f.read()
            self.settings["web"] = yaml.load(s, Loader)
        if populate: self.populateConfig(reload)

    def populateConfig(self, reload=False):
        # Send the configuration to the respective factories
        if self.serverType == SERVER_TYPES["HubServer"]:
            self.factories["MinecraftHubServerFactory"].settings = self.settings["hub"]
            self.factories["WorldServerCommServerFactory"].settings = self.settings["hub"]
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            self.factories["WorldServerFactory"].settings = self.settings["world"]
        elif self.serverType == SERVER_TYPES["WebServer"]:
            self.factories["WebServerApplication"].settings = self.settings["web"]

    def loadDatabase(self):
        """
        Connects to the database.
        """
        connArgs = []
        connKwargs = dict()
        try:
            __import__(("%s" % self.settings["common"]["db"]["driver"]))
        except ImportError:
            self.logger.critical("Database module {dbModule} not found, stopping.".format(dbModule=self.settings["common"]["db"]["driver"]))
            self.stop()
        if self.settings["common"]["db"]["driver"] == "sqlite3":
            connKwargs["database"] = self.settings["common"]["db"]["driver-config"]["file"]
            databaseProxy.initialize(SqliteDatabase(None))
        # TODO Implement
        elif self.settings["common"]["db"]["driver"] == "txmysql":
            connKwargs = {}
            databaseProxy.initialize(MySQLDatabase(None))
        elif self.settings["common"]["db"]["driver"] == "txpostgres":
            connKwargs = {}
            databaseProxy.initialize(PostgresqlDatabase(None))
        elif self.settings["common"]["db"]["driver"] == "MySQLdb":
            from MySQLdb.cursors import DictCursor
            connKwargs = {
                "host": self.settings["common"]["db"]["driver-config"]["server-ip"],
                "db": self.settings["common"]["db"]["driver-config"]["database"],
                "user": self.settings["common"]["db"]["driver-config"]["username"],
                "passwd": self.settings["common"]["db"]["driver-config"]["password"],
                "cursorclass": DictCursor
            }
            databaseProxy.initialize(MySQLDatabase(None))
        elif self.settings["common"]["db"]["driver"] == "psycopg2":
            connKwargs = {}
            databaseProxy.initialize(PostgresqlDatabase(None))
        self.db = ConnectionPool(self.settings["common"]["db"]["driver"], *connArgs, **connKwargs)
        # Perform basic validation check
        self.db.runQuery(GlobalMetadata.select(GlobalMetadata.value).where(GlobalMetadata.name == "databaseVersion").sql()).addBoth(self.checkTablesCallabck)

    def checkTablesCallabck(self, res):
        checkForFailure(res)
        if isinstance(res, Failure):
            self.stop()
        elif not res:
            self.logger.critical("Database validation chck failed: databaseVersion row not found in cb_global_metadata.")
            self.logger.critical("Maybe the database is corrupt?")
            self.stop()
        elif int(res[0]["value"]) != VERSION_NUMBER:
            self.logger.critical("Database validation check failed: Database version and software version mismatch.")
            self.logger.critical("Software version: {softwareVersion}, Database version: {dbVersion}".format(softwareVersion=VERSION_NUMBER, dbVersion=res[0]["value"]))
            self.stop()
        else:
            self.logger.info("Database API ready.")

    def start(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import init as hubInit
            hubInit(self)
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            from cloudbox.world.run import init as worldInit
            worldInit(self)
        elif self.serverType == SERVER_TYPES["WebServer"]:
            from cloudbox.web.run import init as webInit
            webInit(self)

    def stop(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import shutdown as hubShutdown
            hubShutdown(self)
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            from cloudbox.world.run import shutdown as worldShutdown
            worldShutdown(self)
        elif self.serverType == SERVER_TYPES["WebServer"]:
            from cloudbox.web.run import shutdown as webShutdown
            webShutdown(self)