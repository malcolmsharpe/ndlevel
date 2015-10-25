import os.path

from dungeon import *

name = 'GENDUNG1'

dungeon = Dungeon()
dungeon.name = name

level = Level()
dungeon.put_level(level)

level.put_rect(-3, 4, -3, 4, 0, Tile.WALL_DIRT)
level.put_rect(-2, 3, -2, 3, 0, Tile.FLOOR)

# Write
ndpath = file('ndpath.txt', 'r').read().strip()
outpath = os.path.join(ndpath, 'dungeons', name + '.xml')

dungeon.write( file(outpath, 'w') )
print 'Wrote dungeon to %s' % outpath
