# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Factory

from cloudbox.database.server.protocol import DatabaseServerProtocol


class DatabaseServerFactory(Factory):
    """I am a database server that takes requests from nodes."""

    protocol = DatabaseServerProtocol

    def __init__(self, dbProvider):
        self.loadConfig()
        self.dbProvider = dbProvider(self)

    def loadConfig(self):
        """
        Loads the configuration.
        """
        self.settings = yaml.load("../config/database.yaml", Loader)