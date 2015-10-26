import random

from dungeon import *

def get_enemy_pool(floor):
    # Missing Ghost, maybe some other 1-1 enemies.
    enemy_pool = [Enemy.SLIME_BLUE, Enemy.SKELETON_WHITE, Enemy.BAT_BLUE, Enemy.MONKEY_PURPLE, Enemy.WRAITH,
        Enemy.ZOMBIE]

    if floor >= 1:
        # medium difficulty z1 enemies

        enemy_pool.extend(
            [Enemy.SLIME_ORANGE, Enemy.SKELETON_YELLOW, Enemy.BAT_RED] )

    if floor >= 2:
        # hard difficulty z1 enemies

        enemy_pool.extend(
            [Enemy.MONKEY_WHITE, Enemy.SKELETON_BLACK] )

    return enemy_pool

def randomly_put_enemies(level, enemy_pool, available, pop_per_room):
    random.shuffle(available)
    for (ex, ey) in available[:pop_per_room]:
        et = random.choice(enemy_pool)
        level.put_enemy( Enemy(ex, ey, et) )

def random_miniboss_type(floor):
    if floor == 0:
        miniboss_pool = [Enemy.DIREBAT_YELLOW, Enemy.DRAGON_GREEN, Enemy.MINOTAUR_LIGHT]
    else:
        miniboss_pool = [Enemy.DRAGON_RED, Enemy.MINOTAUR_DARK]
        if floor < 2:
            miniboss_pool.append(Enemy.DIREBAT_GRAY)

    return random.choice(miniboss_pool)
