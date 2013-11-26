# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import random

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.constants import handlers


class FetchDataHandler(BasePacketHandler):
    @staticmethod
    def packData(data):
        return data["packer"].pack([
            handlers.TYPE_FETCH_DATA,
            data["requestID"],
            data["model"],  # Model name
            data["fields"],
            data["condition"],
            data["extraClauses"],
            data["interpolation"],
            data["extraParameters"]
        ])

    @staticmethod
    def handleData(data):
        requestID, model, fields, condition, extraClauses, interpolation, extraParameters = data["packetData"][1:]


class DirectQueryHandler(BasePacketHandler):
    @staticmethod
    def packData(data):
        return data["packer"].pack([
            handlers.TYPE_DIRECT_QUERY,
            data["requestID"],
            data["query"],
            data["interpolation"],
            data["extraParameters"],  # ???
            data["isOperation"]  # Set to true to have the server run this as an operation
        ])

    @staticmethod
    def handleData(data):
        requestID, query, interpolation, extraParameters, isOperation = data["packetData"][1:]
        if not requestID:
            f = data["parent"].factory.dbapi.runOperation
        else:
            f = data["parent"].factory.dbapi.runQuery
        d = f(query, interpolation, extraParameters).addCallback(data["parent"].standardQueryCallback, requestID)
        # Make a copy in the protocol requests dict and in the master list.
        data["parent"]


class QueryResultHandler(BasePacketHandler):
    @classmethod
    def packData(data):
        l = [
            handlers.TYPE_QUERY_RESULT,
            data["result"],
        ]
        if not data["isOperation"]:
            l.append(data["resource"])
        return data["packer"].pack(l)