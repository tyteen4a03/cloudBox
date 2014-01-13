# cloudBox is copyright 2012 - 2013 the cloudBox team.
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

from cloudbox.common.loops import LoopRegistry
from cloudbox.common.constants.common import *


class CloudBoxService(object):
    """
    The central hub of all services.
    """

    def __init__(self, whoami):
        """
        Initializes the service.
        Whoami contains the server identifier.
        """
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