# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

"""
Constants for World Servers.
"""

SUPPORTED_WORLD_TYPES = {
    "classic": {
        "fullname": "Classic",
        "finite": True,
        "format": ("cloudbox.world.worlds.classic", "ClassicWorld")
    },
    # TODO Support everything!
    # "modern_survival": {
    #     "fullname": "Modern (Survival Mode)",
    #     "finite": False,
    #     "format": ("cloudbox.world.worlds.modern.survival", "ModernSurvivalWorld")
    # },
    # "modern_creative": {
    #     "fullname": "Modern (Creative Mode)",
    #     "finite": False,
    #     "format": ("cloudbox.world.worlds.modern.creative", "ModernCreativeWorld")
    # },
    # "pocket_survival": {
    #     "fullname": "Pocket Edition (Survival Mode)",
    #     "finite": False,
    #     "format": ("cloudbox.world.worlds.pe.survival", "PESurvivalWorld")
    # },
    # "pocket_creative": {
    #     "fullname": "Pocket Edition (Creative Mode)",
    #     "finite": False,
    #     "format": ("cloudbox.world.worlds.pe.creative", "PECreativeWorld")
    # }
}

SUPPORTED_WORLD_FORMATS = {
    "cw": {
        "fullname": "ClassicWorld",
        "format": ("cloudbox.common.world.formats.cw", "ClassicWorldWorldFormat")
    }
}