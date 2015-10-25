# Backend to write XML dungeons.

class Dungeon(object):
    def __init__(self):
        self.name = 'UNTITLED'
        self.levels = []

    def write(self, f):
        print >>f, '<?xml?>'
        print >>f, '<dungeon character="-1" name="%s" numLevels="%d">' % (self.name, len(self.levels))

        for i, level in enumerate(self.levels):
            level.write(f, i)

        print >>f, '</dungeon>'

    def put_level(self, level):
        self.levels.append(level)

class Level(object):
    def __init__(self):
        self.music = 0
        self.tiles = {} # (x,y) -> tile
        self.enemies = []

    def write(self, f, i):
        print >>f, '<level bossNum="-1" music="%d" num="%d">' % (self.music, i + 1)

        print >>f, '<tiles>'
        for tile in self.tiles.values():
            tile.write(f)
        print >>f, '</tiles>'

        print >>f, '<traps>'
        print >>f, '</traps>'

        print >>f, '<enemies>'
        for enemy in self.enemies:
            enemy.write(f)
        print >>f, '</enemies>'

        print >>f, '<items>'
        print >>f, '</items>'

        print >>f, '<chests>'
        print >>f, '</chests>'

        print >>f, '<crates>'
        print >>f, '</crates>'

        print >>f, '<shrines>'
        print >>f, '</shrines>'

        print >>f, '</level>'

    def put_tile(self, tile):
        self.tiles[ (tile.x, tile.y) ] = tile

    def put_enemy(self, enemy):
        self.enemies.append(enemy)

    def put_rect(self, x_lo, x_hi, y_lo, y_hi, zone, type, torch=0):
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
        print >>f, '<tile torch="%d" type="%d" x="%d" y="%d" zone="%d"></tile>' % (
            self.torch, self.type, self.x, self.y, self.zone)

class Enemy(object):
    SLIME_GREEN = 0
    SLIME_BLUE = 1
    SLIME_ORANGE = 2
    SKELETON_WHITE = 3
    SKELETON_YELLOW = 4
    SKELETON_BLACK = 5
    BAT_BLUE = 6
    BAT_RED = 7
    MONKEY_PURPLE = 9
    MONKEY_WHITE = 10
    ZOMBIE = 12
    WRAITH = 13

    DIREBAT_YELLOW = 400
    DIREBAT_GRAY = 401
    DRAGON_GREEN = 402
    DRAGON_RED = 403
    MINOTAUR_LIGHT = 407
    MINOTAUR_DARK = 408

    def __init__(self, x, y, type, beatDelay=1, lord=0):
        self.x = x
        self.y = y
        self.type = type
        self.beatDelay = beatDelay
        self.lord = lord

    def write(self, f):
        print >>f, '<enemy beatDelay="%d" lord="%d" type="%d" x="%d" y="%d"></enemy>' % (
            self.beatDelay, self.lord, self.type, self.x, self.y)
