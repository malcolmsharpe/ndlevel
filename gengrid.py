import os.path
import random

from dungeon import *
from util import *

name = 'AGENDUNG1'

dungeon = Dungeon()
dungeon.name = name

def gen_grid_level(floor):
    level = Level()

    # Generate a 3x3 grid of 5x5 rooms.
    # Connected by corridors of length 3.

    ROOM_WIDTH = 5
    ROOM_SPREAD = (ROOM_WIDTH - 1) // 2
    PADDING = 3
    INCR = ROOM_WIDTH + PADDING
    POP_PER_ROOM = 5

    enemy_pool = get_enemy_pool(floor)

    X = 6
    Y = 3

    level.put_rect(
        - ROOM_SPREAD - 1, INCR * (X-1) + ROOM_SPREAD + 2,
        - ROOM_SPREAD - 1, INCR * (Y-1) + ROOM_SPREAD + 2,
        0, Tile.WALL_STONE)

    for x in range(X):
        for y in range(Y):
            x_0 = INCR * x
            y_0 = INCR * y

            x1 = x_0 - ROOM_SPREAD
            x2 = x_0 + ROOM_SPREAD + 1
            y1 = y_0 - ROOM_SPREAD
            y2 = y_0 + ROOM_SPREAD + 1

            level.put_rect(
                x1 - 1, x2 + 1,
                y1 - 1, y2 + 1,
                0, Tile.WALL_DIRT)
            level.put_rect(
                x1, x2,
                y1, y2,
                0, Tile.FLOOR)

            if x != 0 or y != 0:
                # Put some enemies in the room.
                available = []
                for ex in range(x1, x2):
                    for ey in range(y1, y2):
                        # The exit room reserves the middle tile for the stairs and miniboss.
                        if (x,y) != (X-1, Y-1) or (ex,ey) != (x_0,y_0):
                            available.append( (ex, ey) )

                randomly_put_enemies(level, enemy_pool, available, POP_PER_ROOM)

    P_COR_DOOR = 0.5

    for x in range(X):
        for y in range(Y):
            x_0 = INCR * x
            y_0 = INCR * y

            x_1 = INCR * (x+1)
            y_1 = INCR * (y+1)

            # vertical corridor
            if y + 1 < Y:
                cor_x = x_0 + random.randrange(-1, 2)

                level.put_rect(
                    cor_x - 1, cor_x + 2,
                    y_0 + ROOM_SPREAD + 1, y_1 - ROOM_SPREAD,
                    0, Tile.WALL_DIRT)
                level.put_rect(
                    cor_x, cor_x + 1,
                    y_0 + ROOM_SPREAD + 1, y_1 - ROOM_SPREAD,
                    0, Tile.FLOOR)

                if random.random() < P_COR_DOOR:
                    level.put_tile( Tile(cor_x, y_0 + ROOM_SPREAD + 2, 0, Tile.DOOR) )

            # horizontal corridor
            if x + 1 < X:
                cor_y = y_0 + random.randrange(-1, 2)

                level.put_rect(
                    x_0 + ROOM_SPREAD + 1, x_1 - ROOM_SPREAD,
                    cor_y - 1, cor_y + 2,
                    0, Tile.WALL_DIRT)
                level.put_rect(
                    x_0 + ROOM_SPREAD + 1, x_1 - ROOM_SPREAD,
                    cor_y, cor_y + 1,
                    0, Tile.FLOOR)

                if random.random() < P_COR_DOOR:
                    level.put_tile( Tile(x_0 + ROOM_SPREAD + 2, cor_y, 0, Tile.DOOR) )

    exit_x = INCR * (X-1)
    exit_y = INCR * (Y-1)
    level.put_tile( Tile(exit_x, exit_y, 0, Tile.STAIRS_LOCKED) )

    miniboss_type = random_miniboss_type(floor)
    level.put_enemy( Enemy(exit_x, exit_y, miniboss_type) )

    # Make 1/3rd of dirt walls have torches at random.
    # This is the proportion in the default level editor room.
    for tile in level.tiles.values():
        if tile.type == Tile.WALL_DIRT and random.randrange(3) == 0:
            tile.torch = 1

    return level

LEVELS = 3

for floor in range(LEVELS):
    level = gen_grid_level(floor)
    level.music = floor
    dungeon.put_level(level)

# Write
ndpath = file('ndpath.txt', 'r').read().strip()
outpath = os.path.join(ndpath, 'dungeons', name + '.xml')

dungeon.write( file(outpath, 'w') )
print('Wrote dungeon to %s' % outpath)
