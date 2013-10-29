# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import sys

from cloudbox.common.logger import Logger
from cloudbox.common.service import CloudBoxService
from cloudbox.common.constants.common import *

if sys.argv[1] not in SERVER_TYPES.keys():
    raise Exception("ServerType not recognized")

logger = Logger(True)
try:
    from colorama import init
except ImportError:
    logger.warn("Colorama is not installed - console colours DISABLED.")
except Exception as e:
    logger.warn("Unable to import colorama: %s" % e)
    logger.warn("Console colours DISABLED.")
else:
    init()
    logger.stdout("&f")
    logger.debug("&fIf you see this, debug mode is &eon&f!")
    logger.info("&fColorama &ainstalled&f - Console colours &cENABLED&f.")
logger.info("Starting cloudBox %s Version %s" % (sys.argv[1], VERSION))

# TODO - Less hack required
try:
    service = CloudBoxService(sys.argv[1])
    service.start()
except (KeyboardInterrupt, SystemExit):
    service.stop()