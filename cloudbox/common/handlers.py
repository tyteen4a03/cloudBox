# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import implements

from cloudbox.common.interfaces import IDataHandler

class HandshakeRequestDataHandler(object):
    """
    DataHandler for packet HandshakeRequest.
    """

    implements(IDataHandler)

    def __init__(self):
