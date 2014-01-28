# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Attribute, Interface


class IPlugin(Interface):
    """
    An interface to all plugins.
    """

    name = Attribute("""Name of the plugin""")
    version = Attribute("""Version of the plugin""")


class ICommand(Interface):
    """
    An interface for all commands.
    """

    name = Attribute("""Name of the command""")
    aliases = Attribute("""Aliases of the command, if any""")

    def runCommand(parent, data):


class IPlayerCommand(ICommand):
    """
    An Interface for all Player Commands.
    """
