# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from functools import wraps
from logging import getLogger

from twisted.python.failure import Failure

logger = getLogger("cloudbox.database.error")


def checkForFailure(res):
    if isinstance(res, Failure):
        logger.error("Database query error:")
        logger.error(res.getTraceback())