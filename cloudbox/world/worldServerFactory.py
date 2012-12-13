# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import Factory
from cloudbox.common.logger import Logger
from cloudbox.common.centralLogger.pipe import CentralLoggerPipe

class WorldServerFactory(Factory):
    """
    I am the world server. I host some worlds, and do calculations about them.
    """
    pass