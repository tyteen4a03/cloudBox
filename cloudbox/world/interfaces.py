# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Attribute, Interface


class IWorld(Interface):
    """
    I am a World.
    """

    blockData = Attribute("Actual world data. A 3D array.")

    def loadWorld():
        """
        Loads the world into memory for use.
        """

    def saveWorld():
        """
        Saves the world from memory to disk, or to a stream.
        """


class IWorldLoader(Interface):
    """
    I am a World Loader.
    """

    name = Attribute("The name of the world loader.")
    supportsLoading = Attribute("Whether I support loading worlds from the format I support.")
    supportsSaving = Attribute("Whether I support saving worlds as the format I support.")

    worldStorageFormat = Attribute("How this world is stored. Valid values are: file, directory, stream")
    fileExtensions = Attribute("List of file extensions this WorldFormat supports. If it's a directory, set as None.")

    def loadWorld():
        """
        Loads a world from filepath. Returns a dictionary that follows the ClassicWorld format
        (see docs/worldFormat and docs/worldFormat-CPE)
        This function is allowed to block.
        """

    def saveWorld(data):
        """
        Saves a world from filepath, using data given. Data is a dictionary that follows the ClassicWorld format.
        This function is allowed to block.
        """
