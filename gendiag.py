# Layouts following this room layout idea:
#    X-X
#    | |
#    X-X-X
#      | |
#      X-X-X
#        | |
#        X-X
# The top-left is the entrance and the bottom-right is the exit.
# Some rooms are on the main path and must be visited, but the player is also given a choice each
# time the path splits.

from collections import namedtuple
import os.path
import random

from dungeon import *
from util import *

name = 'AGENDUNG1'

dungeon = Dungeon()
dungeon.name = name

Room = namedtuple('Room', ['x_lo', 'x_hi', 'y_lo', 'y_hi'])

def gen_diag_level(floor):
    level = Level()

    # Currently only generating zone 1 layouts with this method.
    zone = 0

    INIT_ROOM_WIDTH = 5
    INIT_ROOM_HEIGHT = 5

    # These ranges are the same as the original game's zone 1 level generation.
    ROOM_MIN_WIDTH = 5
    ROOM_MAX_WIDTH = 7
    ROOM_MIN_HEIGHT = 4
    ROOM_MAX_HEIGHT = 6

    PADDING = 3
    POP_PER_ROOM = 5

    enemy_pool = get_enemy_pool(floor)

    LAYERS = 3

    # First pass is to determine all room locations.
    # The first room will be the starting room.
    main_rooms = []
    up_rooms = []
    down_rooms = []

    next_top = - (INIT_ROOM_HEIGHT - 1) // 2
    next_left = - (INIT_ROOM_WIDTH - 1) // 2

    for i in range(LAYERS + 1):
        # Place the main path room.
        if i == 0:
            main_width = INIT_ROOM_WIDTH
            main_height = INIT_ROOM_HEIGHT
        else:
            main_width = random.randrange(ROOM_MIN_WIDTH, ROOM_MAX_WIDTH + 1)
            main_height = random.randrange(ROOM_MIN_HEIGHT, ROOM_MAX_HEIGHT + 1)

        main_room = Room(next_left, next_left + main_width, next_top, next_top + main_height)
        main_rooms.append(main_room)

        if i == LAYERS:
            # The previous room placed was the exit room.
            break

        # Place the off-diagonal rooms.

        # To make an appropriate space for the next main diagonal room, one of the off-diagonal rooms needs
        # to extend at least as far as the previous main diagonal room. However, not both of them can extend
        # farther, or they would overlap.
        up_top = main_room.y_lo
        up_left = main_room.x_hi + PADDING
        up_width = random.randrange(ROOM_MIN_WIDTH, ROOM_MAX_WIDTH + 1)

        down_top = main_room.y_hi + PADDING
        down_left = main_room.x_lo
        down_height = random.randrange(ROOM_MIN_HEIGHT, ROOM_MAX_HEIGHT + 1)

        if random.randrange(2) == 0:
            up_height = random.randrange(main_height, ROOM_MAX_HEIGHT + 1)
            down_width = random.randrange(ROOM_MIN_WIDTH, main_width + 1)
        else:
            up_height = random.randrange(ROOM_MIN_HEIGHT, main_height + 1)
            down_width = random.randrange(main_width, ROOM_MAX_WIDTH + 1)

        up_room = Room(up_left, up_left + up_width, up_top, up_top + up_height)
        down_room = Room(down_left, down_left + down_width, down_top, down_top + down_height)

        up_rooms.append(up_room)
        down_rooms.append(down_room)

        next_top = up_room.y_hi + PADDING
        next_left = down_room.x_hi + PADDING

    # Put the room tiles.
    for room in main_rooms + up_rooms + down_rooms:
        level.put_rect(
            room.x_lo - 2, room.x_hi + 2,
            room.y_lo - 2, room.y_hi + 2,
            zone, Tile.WALL_STONE)

        level.put_rect(
            room.x_lo - 1, room.x_hi + 1,
            room.y_lo - 1, room.y_hi + 1,
            zone, Tile.WALL_DIRT)

        level.put_rect(
            room.x_lo, room.x_hi,
            room.y_lo, room.y_hi,
            zone, Tile.FLOOR)

    # Put the level exit.
    exit_room = main_rooms[-1]
    exit_x = (exit_room.x_lo + exit_room.x_hi) // 2
    exit_y = (exit_room.y_lo + exit_room.y_hi) // 2
    level.put_tile( Tile(exit_x, exit_y, zone, Tile.STAIRS_LOCKED) )

    miniboss_type = random_miniboss_type(floor)
    level.put_enemy( Enemy(exit_x, exit_y, miniboss_type) )

    # Make 1/6rd of dirt walls have torches at random.
    # This is the density in actual generation, but it uses a different algorithm to place them.
    for tile in level.tiles.values():
        if tile.type == Tile.WALL_DIRT and random.randrange(6) == 0:
            tile.torch = 1

    return level

LEVELS = 3

for floor in range(LEVELS):
    level = gen_diag_level(floor)
    level.music = floor
    dungeon.put_level(level)

# Write
ndpath = file('ndpath.txt', 'r').read().strip()
outpath = os.path.join(ndpath, 'dungeons', name + '.xml')

dungeon.write( file(outpath, 'w') )
print 'Wrote dungeon to %s' % outpath
