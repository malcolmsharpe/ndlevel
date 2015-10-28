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

Room = namedtuple('Room', ['x_lo', 'x_hi', 'y_lo', 'y_hi', 'type'])

PADDING = 3

ROOM_ENTRY = 'room_entry'
ROOM_EXIT = 'room_exit'
ROOM_OTHER = 'room_other'
ROOM_ITEM = 'room_item'

miniboss_pool = MinibossPool()
item_pool = ItemPool()

def gen_diag_level(floor):
    level = Level()

    # Currently only generating zone 1 layouts with this method.
    zone = 0

    INIT_ROOM_WIDTH = 5
    INIT_ROOM_HEIGHT = 5

    ITEM_ROOM_WIDTH = 5
    ITEM_ROOM_HEIGHT = 5
    ITEM_ROOM_POST_SHIFT_X = 2
    ITEM_ROOM_POST_SHIFT_Y = 0
    ITEM_POS = [(1,0), (2,1), (3,0)]

    # These ranges are the same as the original game's zone 1 level generation.
    ROOM_MIN_WIDTH = 5
    ROOM_MAX_WIDTH = 7
    ROOM_MIN_HEIGHT = 4
    ROOM_MAX_HEIGHT = 6

    enemy_pool = get_enemy_pool(floor)

    LAYERS = 3

    # Probabilities of certain room decorations (mutually exclusive).
    # These are only loosely based on the frequency in the original game.
    P_POSTS = 0.2
    P_INWARD_CORNERS = 0.4

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

        room_type = ROOM_OTHER
        if i == 0:
            room_type = ROOM_ENTRY
        if i == LAYERS:
            room_type = ROOM_EXIT

        main_room = Room(next_left, next_left + main_width, next_top, next_top + main_height, room_type)
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

        up_room = Room(up_left, up_left + up_width, up_top, up_top + up_height, ROOM_OTHER)
        down_room = Room(down_left, down_left + down_width, down_top, down_top + down_height, ROOM_OTHER)

        up_rooms.append(up_room)
        down_rooms.append(down_room)

        next_top = up_room.y_hi + PADDING
        next_left = down_room.x_hi + PADDING

    # A room at the end for the player to select an item.
    # Since the exit room's minimum height is 4, and the item room has height 5, it always fits provided
    # its bottom edge is shifted down by 1 relative to the exit room.
    exit_room = main_rooms[-1]
    item_room_x_lo = exit_room.x_hi + PADDING
    item_room_y_hi = exit_room.y_hi + 1
    item_room = Room(
        item_room_x_lo, item_room_x_lo + ITEM_ROOM_WIDTH,
        item_room_y_hi - ITEM_ROOM_HEIGHT, item_room_y_hi,
        ROOM_ITEM)

    # Put the room tiles.
    for room in main_rooms + up_rooms + down_rooms + [item_room]:
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

        if room.type not in [ROOM_ENTRY, ROOM_ITEM]:
            # Decorate the room (maybe) with some extra walls.
            # (The wall type could be made random instead.)
            deco = random.random()

            if 0 <= deco < P_POSTS:
                post_xs = [room.x_lo + 1, room.x_hi - 2]
                post_ys = [room.y_lo + 1, room.y_hi - 2]

                for x in post_xs:
                    for y in post_ys:
                        level.put_tile( Tile(x, y, zone, Tile.WALL_STONE) )
            elif deco < P_POSTS + P_INWARD_CORNERS:
                corner_xs = [room.x_lo, room.x_hi - 1]
                corner_ys = [room.y_lo, room.y_hi - 1]

                for x in corner_xs:
                    for y in corner_ys:
                        level.put_tile( Tile(x, y, zone, Tile.WALL_DIRT) )

        if room.type == ROOM_ITEM:
            # This has 1 extra wall, like the original game's boss chest area.
            level.put_tile( Tile(
                room.x_lo + ITEM_ROOM_POST_SHIFT_X,
                room.y_lo + ITEM_ROOM_POST_SHIFT_Y,
                zone, Tile.WALL_DIRT) )

    # Connect the rooms with corridors.
    for i in range(LAYERS):
        put_corridor(level, zone, main_rooms[i], up_rooms[i])
        put_corridor(level, zone, main_rooms[i], down_rooms[i])
        put_corridor(level, zone, up_rooms[i], main_rooms[i+1])
        put_corridor(level, zone, down_rooms[i], main_rooms[i+1])
    put_corridor(level, zone, exit_room, item_room)

    # Put the level exit.
    exit_x = (exit_room.x_lo + exit_room.x_hi) // 2
    exit_y = (exit_room.y_lo + exit_room.y_hi) // 2
    level.put_tile( Tile(exit_x, exit_y, zone, Tile.STAIRS_LOCKED) )

    miniboss_type = miniboss_pool.pick(floor)
    level.put_enemy( Enemy(exit_x, exit_y, miniboss_type) )

    # Populate all non-entry, non-item rooms.
    for room in main_rooms[1:] + up_rooms + down_rooms:
        available = []
        for x in range(room.x_lo, room.x_hi):
            for y in range(room.y_lo, room.y_hi):
                if level.tiles[(x,y)].type == Tile.FLOOR:
                    available.append( (x,y) )

        pop_per_room = 5 + floor
        if room.type == ROOM_EXIT:
            pop_per_room += 3

        randomly_put_enemies(level, enemy_pool, available, pop_per_room)

    # Put items in the item room.
    for i, (dx,dy) in enumerate(ITEM_POS):
        item_type = item_pool.pick(floor, i)
        level.put_item( Item(item_room.x_lo + dx, item_room.y_lo + dy, item_type, singleChoice=1) )

    # Make 1/6rd of dirt walls have torches at random.
    # This is the density in actual generation, but it uses a different algorithm to place them.
    TORCH_AVG = 6
    for tile in level.tiles.values():
        if tile.type == Tile.WALL_DIRT and random.randrange(TORCH_AVG) == 0:
            tile.torch = 1

    return level

def put_corridor(level, zone, room_a, room_b):
    # Put a passage between these two rooms. If that's not possible, crash.

    P_DOOR = 0.5

    x_lo = max(room_a.x_lo, room_b.x_lo)
    x_hi = min(room_a.x_hi, room_b.x_hi)
    y_lo = max(room_a.y_lo, room_b.y_lo)
    y_hi = min(room_a.y_hi, room_b.y_hi)

    vert = x_lo < x_hi
    horz = y_lo < y_hi

    assert vert or horz
    assert (not vert) or (not horz)

    if horz:
        assert x_lo - x_hi == PADDING
        co_x_lo = x_hi - 1
        co_x_hi = x_lo + 1
        co_y_lo = random.randrange(y_lo, y_hi)
        co_y_hi = co_y_lo + 1

        wa_x_lo = x_hi
        wa_x_hi = x_lo
        wa_y_lo = co_y_lo - 1
        wa_y_hi = co_y_hi + 1

        dr_x = random.choice( [x_hi, x_lo - 1] )
        dr_y = co_y_lo
    else: # vert
        assert y_lo - y_hi == PADDING
        co_x_lo = random.randrange(x_lo, x_hi)
        co_x_hi = co_x_lo + 1
        co_y_lo = y_hi - 1
        co_y_hi = y_lo + 1

        wa_x_lo = co_x_lo - 1
        wa_x_hi = co_x_hi + 1
        wa_y_lo = y_hi
        wa_y_hi = y_lo

        dr_x = co_x_lo
        dr_y = random.choice( [y_hi, y_lo - 1] )

    # Make the corridor's border walls consistently dirt. It's prettier that way.
    level.put_rect(
        wa_x_lo, wa_x_hi,
        wa_y_lo, wa_y_hi,
        zone, Tile.WALL_DIRT)

    # The corridor itself.
    level.put_rect(
        co_x_lo, co_x_hi,
        co_y_lo, co_y_hi,
        zone, Tile.FLOOR)

    # Maybe put in a door.
    if random.random() < P_DOOR:
        level.put_tile( Tile(dr_x, dr_y, zone, Tile.DOOR) )

LEVELS = 3

for floor in range(LEVELS):
    level = gen_diag_level(floor)
    level.music = floor
    dungeon.put_level(level)

# Write
ndpath = file('ndpath.txt', 'r').read().strip()
outpath = os.path.join(ndpath, 'dungeons', name + '.xml')

dungeon.write( file(outpath, 'w') )
print('Wrote dungeon to %s' % outpath)
