# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.constants.common import ERRORS
from cloudbox.common.exceptions import ErrorCodeException


class WorldServerLinkException(ErrorCodeException):
    pass


class WorldServerLinkNotEstablishedException(WorldServerLinkException):
    errorCode = ERRORS["worldserver_link_not_established"]


class NoResultsException(ErrorCodeException):
    errorCode = ERRORS["no_results"]