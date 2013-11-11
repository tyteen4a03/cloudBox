# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.python.failure import Failure


class _errorCodeException(Exception):
    """
    An exception with an error code and optionally an error message.
    """
    errorCode = None
    errorMessage = None

    def __init__(self, errorCode, errorMessage=""):
        self.errorCode = errorCode
        self.errorMessage = errorMessage

    def __repr__(self):
        return "Error {1}: {2}".format(self.errorCode, self.errorMessage)

    __str__ = __repr__


def makeFailure(cls, errorCode, errorMessage=""):
    return cls(errorCode, errorMessage)