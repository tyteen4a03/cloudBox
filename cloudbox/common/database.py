# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import itertools
from functools import wraps
from logging import getLogger

import MySQLdb
from twisted.enterprise import adbapi
from twisted.python import log, failure


logger = getLogger("cloudbox.database.error")


def hasFailed(res):
    if isinstance(res, failure.Failure):
        logger.error("Database query error:")
        logger.error(res.getTraceback())
        return True
    return False


class InsertIDMixin:
    def runMySQLInsert(self, *args, **kw):
        return self.runInteraction(self._runMySQLInsert, *args, **kw)

    def _runMySQLInsert(self, trans, *args, **kw):
        trans.execute(*args, **kw)
        return trans.connection.insert_id()


class ConnectionPool(InsertIDMixin, adbapi.ConnectionPool):
    pass