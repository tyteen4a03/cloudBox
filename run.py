# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import logging
import logging.config
import sys

from cloudbox.common.service import CloudBoxService
from cloudbox.common.constants.common import *

if sys.argv[1] not in SERVER_TYPES.keys():
    raise Exception("ServerType not recognized")

logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)-15s [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': (logging.DEBUG if "--debug" in sys.argv else logging.INFO),
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            "handlers": ["default"],
            "level": (logging.DEBUG if "--debug" in sys.argv else logging.INFO),
            "propagate": True,
        }
    }
})

# TODO - Less hack required?
service = CloudBoxService(sys.argv[1])
service.logger = logging.getLogger("cloudbox")
service.logger.info("Starting cloudBox %s Version %s" % (sys.argv[1], VERSION))
service.logger.debug("Debug mode ON.")
try:
    service.start()
except (KeyboardInterrupt, SystemExit):
    service.stop()