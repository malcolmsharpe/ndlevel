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

class ItemPool(object):
    KIND_RED = 0
    KIND_PURPLE = 1
    KIND_BLACK = 2
    NKIND = 3

    # TODO: Put more items here, and account for item strength somehow.
    POOLS = {
        KIND_RED: [
            'food_1',
            'food_2',
            'food_3',
            'food_4',
            'holy_water',
        ],
        KIND_PURPLE: [
            'ring_courage',
            'ring_war',
            'ring_mana',
            'ring_might',
            'ring_luck',
            'ring_phasing',
            'ring_regeneration',
            'ring_protection',
            'ring_shielding',
            'ring_becoming',
        ],
        KIND_BLACK: [
            'weapon_titanium_dagger',
            'weapon_obsidian_dagger',
            'weapon_golden_dagger',
            'weapon_blood_dagger',
            'weapon_glass_dagger',
            'weapon_dagger_jeweled',
            'weapon_dagger_frost',
            'weapon_dagger_phasing',
            'weapon_broadsword',
            'weapon_titanium_broadsword',
            'weapon_obsidian_broadsword',
            'weapon_golden_broadsword',
            'weapon_blood_broadsword',
            'weapon_glass_broadsword',
            'weapon_longsword',
            'weapon_titanium_longsword',
            'weapon_obsidian_longsword',
            'weapon_golden_longsword',
            'weapon_blood_longsword',
            'weapon_glass_longsword',
            'weapon_whip',
            'weapon_titanium_whip',
            'weapon_obsidian_whip',
            'weapon_golden_whip',
            'weapon_blood_whip',
            'weapon_glass_whip',
            'weapon_spear',
            'weapon_titanium_spear',
            'weapon_obsidian_spear',
            'weapon_golden_spear',
            'weapon_blood_spear',
            'weapon_glass_spear',
            'weapon_rapier',
            'weapon_titanium_rapier',
            'weapon_obsidian_rapier',
            'weapon_golden_rapier',
            'weapon_blood_rapier',
            'weapon_glass_rapier',
            'weapon_bow',
            'weapon_titanium_bow',
            'weapon_obsidian_bow',
            'weapon_golden_bow',
            'weapon_blood_bow',
            'weapon_glass_bow',
            'weapon_crossbow',
            'weapon_titanium_crossbow',
            'weapon_obsidian_crossbow',
            'weapon_golden_crossbow',
            'weapon_blood_crossbow',
            'weapon_glass_crossbow',
            'weapon_flail',
            'weapon_titanium_flail',
            'weapon_obsidian_flail',
            'weapon_golden_flail',
            'weapon_blood_flail',
            'weapon_glass_flail',
            'weapon_cat',
            'weapon_titanium_cat',
            'weapon_obsidian_cat',
            'weapon_golden_cat',
            'weapon_blood_cat',
            'weapon_glass_cat',
            'weapon_blunderbuss',
            'weapon_rifle',
        ],
    }

    def __init__(self):
        self.pools = {}

        for kind in range(self.NKIND):
            self.pools[kind] = []

    def pick(self, floor, kind):
        # TODO: Don't ignore floor (and zone).

        pool = self.pools[kind]
        if len(pool) == 0:
            pool = list(self.POOLS[kind])
            random.shuffle(pool)
            self.pools[kind] = pool
        return pool.pop()
