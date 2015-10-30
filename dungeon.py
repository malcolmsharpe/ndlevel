# Backend to write XML dungeons.

class Dungeon(object):
    def __init__(self):
        self.name = 'UNTITLED'
        self.levels = []

    def write(self, f):
        f.write('<?xml?>\n')
        f.write('<dungeon character="-1" name="%s" numLevels="%d">\n' % (self.name, len(self.levels)))

        for i, level in enumerate(self.levels):
            level.write(f, i)

        f.write('</dungeon>\n')

    def put_level(self, level):
        self.levels.append(level)

class Level(object):
    def __init__(self):
        self.music = 0
        self.tiles = {} # (x,y) -> tile
        self.enemies = []
        self.items = []

    def write(self, f, i):
        f.write('<level bossNum="-1" music="%d" num="%d">\n' % (self.music, i + 1))

        f.write('<tiles>\n')
        # Sorting the tiles serves two purposes:
        # 1. It's easier to inspect the output.
        # 2. Doors can have cosmetic issues in the level editor (not when played) related to where
        #    they appear in the XML. (Unconfirmed guess is that it happens when they show up before both
        #    adjacent walls.)
        for tile in sorted(self.tiles.values(), key=lambda t: (t.x, t.y)):
            tile.write(f)
        f.write('</tiles>\n')

        f.write('<traps>\n')
        f.write('</traps>\n')

        f.write('<enemies>\n')
        for enemy in self.enemies:
            enemy.write(f)
        f.write('</enemies>\n')

        f.write('<items>\n')
        for item in self.items:
            item.write(f)
        f.write('</items>\n')

        f.write('<chests>\n')
        f.write('</chests>\n')

        f.write('<crates>\n')
        f.write('</crates>\n')

        f.write('<shrines>\n')
        f.write('</shrines>\n')

        f.write('</level>\n')

    def put_tile(self, tile):
        self.tiles[ (tile.x, tile.y) ] = tile

    def put_enemy(self, enemy):
        self.enemies.append(enemy)

    def put_item(self, item):
        self.items.append(item)

    def put_rect(self, x_lo, x_hi, y_lo, y_hi, zone, type, torch=0):
        assert x_lo < x_hi
        assert y_lo < y_hi

        for x in range(x_lo, x_hi):
            for y in range(y_lo, y_hi):
                self.put_tile( Tile(x, y, zone, type, torch=torch) )

class Tile(object):
    FLOOR = 0
    STAIRS_UNLOCKED = 2
    WATER = 2
    STAIRS_LOCKED = 9
    WALL_DIRT = 100
    WALL_BORDER = 102
    DOOR = 103
    WALL_STONE = 107
    WALL_CATACOMB = 108
    DOOR_METAL = 111

    def __init__(self, x, y, zone, type, torch=0):
        self.torch = torch
        self.type = type
        self.x = x
        self.y = y
        self.zone = zone

    def write(self, f):
        f.write('<tile torch="%d" type="%d" x="%d" y="%d" zone="%d"></tile>\n' % (
            self.torch, self.type, self.x, self.y, self.zone))

class Enemy(object):
    SLIME_GREEN = 0
    SLIME_BLUE = 1
    SLIME_ORANGE = 2
    SKELETON_WHITE = 3
    SKELETON_YELLOW = 4
    SKELETON_BLACK = 5
    BAT_BLUE = 6
    BAT_RED = 7
    BAT_GREEN = 8
    MONKEY_PURPLE = 9
    MONKEY_WHITE = 10
    GHOST = 11
    ZOMBIE = 12
    WRAITH = 13
    RED_CHEST_MIMIC = 14

    SKELETON_ARMORED_WHITE = 100
    SKELETON_ARMORED_YELLOW = 101
    SKELETON_ARMORED_BLACK = 102
    SKELETON_MAGE_WHITE = 103
    SKELETON_MAGE_YELLOW = 104
    SKELETON_MAGE_BLACK = 105
    MUSHROOM_BLUE = 106
    MUSHROOM_PURPLE = 107
    GOLEM_LIGHT = 108
    GOLEM_DARK = 109
    ARMADILLO_WHITE = 110
    ARMADILLO_YELLOW = 111
    CLONE = 112
    TAR_MONSTER = 113
    MOLE = 114
    WIGHT = 115
    WALL_MIMIC = 116
    MUSHROOM_LIGHT = 117
    MUSHROOM_EXPLODING = 118

    SLIME_FIRE = 200
    SLIME_ICE = 201
    SKELETON_KNIGHT_WHITE = 202
    SKELETON_KNIGHT_YELLOW = 203
    SKELETON_KNIGHT_BLACK = 204
    ELEMENTAL_FIRE = 205
    ELEMENTAL_ICE = 206
    GOBLIN_PURPLE = 207
    GOBLIN_GRAY = 208
    BEETLE_FIRE = 209
    BEETLE_ICE = 210
    HELLHOUND = 211
    SHOVE_MONSTER_PURPLE = 212
    YETI = 213
    GHAST = 214
    CAULDRON_MIMIC_FIRE = 215
    CAULDRON_MIMIC_ICE = 216
    CAULDRON_FIRE = 217
    CAULDRON_ICE = 218
    SHOVE_MONSTER_GRAY = 219

    GOBLIN_BOMBER = 300
    GOBLIN_SENTRY = 301
    BAT_BLACK = 302
    ARMADILLO_ORANGE = 303
    BLADEMASTER_APPRENTICE = 304
    BLADEMASTER_MASTER = 305
    GHOUL = 306
    GOLEM_OOZE = 307
    HARPY = 308
    LICH_WHITE = 309
    LICH_YELLOW = 310
    LICH_BLACK = 311
    MONKEY_GREEN = 312
    MONKEY_MAGIC = 313
    PIXIE = 314
    SARCOPHAGUS_WHITE = 315
    SARCOPHAGUS_YELLOW = 316
    SARCOPHAGUS_BLACK = 317
    SPIDER = 318
    WARLOCK_BLUE = 319
    WARLOCK_NEON = 320
    MUMMY = 321
    GARGOYLE_WIND = 322
    GARGOLYE_CHASE = 323
    GARGOYLE_BOMB = 324
    GARGOYLE_EXPLODING = 325
    GARGOYLE_CRATE = 326
    GARGOYLE_NECRODANCER = 327

    DIREBAT_YELLOW = 400
    DIREBAT_GRAY = 401
    DRAGON_GREEN = 402
    DRAGON_RED = 403
    DRAGON_BLUE = 404
    BANSHEE_BLUE = 405
    BANSHEE_GREEN = 406
    MINOTAUR_LIGHT = 407
    MINOTAUR_DARK = 408
    NIGHTMARE_DARK = 409
    NIGHTMARE_BLOOD = 410
    MOMMY = 411
    OGRE = 412

    def __init__(self, x, y, type, beatDelay=1, lord=0):
        self.x = x
        self.y = y
        self.type = type
        self.beatDelay = beatDelay
        self.lord = lord

    def write(self, f):
        f.write('<enemy beatDelay="%d" lord="%d" type="%d" x="%d" y="%d"></enemy>\n' % (
            self.beatDelay, self.lord, self.type, self.x, self.y))

class Item(object):
    def __init__(self, x, y, type, bloodCost=0.0, saleCost=0, singleChoice=0):
        self.x = x
        self.y = y
        self.type = type
        self.bloodCost = bloodCost
        self.saleCost = saleCost
        self.singleChoice = singleChoice

    def write(self, f):
        f.write('<item bloodCost="%.1f" saleCost="%d" singleChoice="%d" type="%s" x="%d" y="%d"></item>\n' % (
            self.bloodCost, self.saleCost, self.singleChoice, self.type, self.x, self.y))
