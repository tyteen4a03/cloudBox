# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.format import Format

TYPE_INITIAL = 0
TYPE_KEEPALIVE = 1
TYPE_LEVELINIT = 2
TYPE_LEVELDATA = 3
TYPE_LEVELFINALIZE = 4
TYPE_BLOCKCHANGE = 5
TYPE_BLOCKSET = 6
TYPE_SPAWNPLAYER = 7
TYPE_PLAYERPOS = 8
TYPE_PLAYERORT = 11
TYPE_PLAYERDESPAWN = 12
TYPE_MESSAGE = 13
TYPE_ERROR = 14
TYPE_SETUSERTYPE = 15

TYPE_FORMATS = {
    TYPE_INITIAL: Format("bssb"),
    TYPE_KEEPALIVE: Format(""),
    TYPE_LEVELINIT: Format(""),
    TYPE_LEVELDATA: Format("hab"),
    TYPE_LEVELFINALIZE: Format("hhh"),
    TYPE_BLOCKCHANGE: Format("hhhbb"),
    TYPE_BLOCKSET: Format("hhhb"),
    TYPE_SPAWNPLAYER: Format("bshhhbb"),
    TYPE_PLAYERPOS: Format("bhhhbb"),
    TYPE_PLAYERORT: Format("bbb"),
    TYPE_PLAYERDESPAWN: Format("b"),
    TYPE_MESSAGE: Format("bs"),
    TYPE_ERROR: Format("s"),
    TYPE_SETUSERTYPE: Format("bb")
}

# 0 is default (official) name according to Minecraft Wiki, 1+ are aliases
BLOCKS = {
    0: ["air"],
    1: ["stone", "rock"],
    2: ["grass"],
    3: ["dirt", "soil"],
    4: ["cobblestone", "cobble"],
    5: ["plank", "woodplank", "woodenplank"],
    6: ["sapling", "shrub", "tree"],
    7: ["bedrock", "groundrock", "solid"],
    8: ["water"],
    9: ["stillwater"],
    10: ["lava"],
    11: ["stilllava"],
    12: ["sand"],
    13: ["gravel"],
    14: ["goldore", "goldrock"],
    15: ["ironore", "ironrock"],
    16: ["coalore", "coalrock"],
    17: ["wood", "trunk", "stump", "log"],
    18: ["leaves", "leaf", "foliage"],
    19: ["sponge", "sponges"],
    20: ["glass"],
    21: ["redcloth", "red"],
    22: ["orangecloth", "orange"],
    23: ["yellowcloth", "yellow"],
    24: ["limecloth", "lime", "lightgreencloth", "lightgreen", "greenyellowcloth", "greenyellow"],
    25: ["greencloth", "green"],
    26: ["aquagreencloth", "aquagreen", "aquacloth", "aqua", "turquoisecloth", "turquoise", "tealcloth", "teal"],
    27: ["cyancloth", "cyan"],
    28: ["bluecloth", "blue"],
    29: ["purplecloth", "purple"],
    30: ["indigocloth", "indigo"],
    31: ["violetcloth", "violet"],
    32: ["magentacloth", "magenta"],
    33: ["pinkcloth", "pink"],
    34: ["blackcloth", "black", "darkgreycloth", "darkgrey", "darkgraycloth", "darkgray"],
    35: ["greycloth", "grey", "graycloth", "gray"],
    36: ["whitecloth", "white"],
    37: ["dandelion", "yellowflower"],
    38: ["rose", "redflower"],
    39: ["brownmushroom", "mushroom", "shroom", "brownshroom"],
    40: ["toadstool", "redmushroom", "redshroom"],
    41: ["gold", "goldblock"],
    42: ["iron", "ironblock", "steel", "steelblock", "metal", "metalblock"],
    43: ["doubleslab", "doublestep", "doublestair"],
    44: ["slab", "step", "stair"],
    45: ["brick"],
    46: ["tnt", "explosive"],
    47: ["bookshelf", "bookcase", "shelf", "books"],
    48: ["mossstone", "moss", "mossy", "mossystone", "mossycobblestone"],
    49: ["obsidian"]
}

BLOCKS_LOOKUP = {}
for blockID, names in BLOCKS.items():
    for name in names:
       BLOCKS_LOOKUP[name] = blockID

BLOCKS_BY_NAME = {}
for blockID, names in BLOCKS.items():
    BLOCKS_BY_NAME[names[0]] = blockID