import random

from dungeon import *

def get_enemy_pool(floor):
    enemy_pool = [
        Enemy.SLIME_GREEN,
        Enemy.SLIME_BLUE,
        Enemy.SKELETON_WHITE,
        Enemy.BAT_BLUE,
        Enemy.MONKEY_PURPLE,
        Enemy.WRAITH,
        Enemy.GHOST,
        Enemy.ZOMBIE,
        ]

    if floor >= 1:
        # medium difficulty z1 enemies

        enemy_pool.extend([
            Enemy.SLIME_ORANGE,
            Enemy.SKELETON_YELLOW,
            Enemy.BAT_RED,
            ])

    if floor >= 2:
        # hard difficulty z1 enemies

        enemy_pool.extend([
            Enemy.MONKEY_WHITE,
            Enemy.SKELETON_BLACK,
            ])

    return enemy_pool

def randomly_put_enemies(level, enemy_pool, available, pop_per_room):
    random.shuffle(available)
    for (ex, ey) in available[:pop_per_room]:
        et = random.choice(enemy_pool)
        level.put_enemy( Enemy(ex, ey, et) )

# Enemy pool which selects a small number of enemies to populate with this run.
class EnemyPoolRandom(object):
    # Omissions 1:
    # - anything that can't stand freely (spider, tar monster, wall mimic)
    # - sarcophagi
    # - skips part of the level (telemonkey)
    # - goblin sentry
    # - anything that doesn't spawn or only rarely (green bat, mummy)
    # - decoration (cauldrons, light mushrooms)
    # - drops items (chest mimic)

    # (type, cost)
    # Lower-cost enemies can appear in higher numbers.
    ELIGIBLE = [
        (Enemy.SLIME_GREEN, 10),
        (Enemy.SLIME_BLUE, 50),
        (Enemy.SLIME_ORANGE, 50),
        (Enemy.SKELETON_WHITE, 100),
        (Enemy.SKELETON_YELLOW, 150),
        (Enemy.SKELETON_BLACK, 300),
        (Enemy.BAT_BLUE, 150),
        (Enemy.BAT_RED, 250),
        (Enemy.MONKEY_PURPLE, 150),
        (Enemy.MONKEY_WHITE, 300),
        (Enemy.GHOST, 150),
        (Enemy.ZOMBIE, 50),
        (Enemy.WRAITH, 250),
        (Enemy.SKELETON_ARMORED_WHITE, 200),
        (Enemy.SKELETON_ARMORED_YELLOW, 250),
        (Enemy.SKELETON_ARMORED_BLACK, 400),
        (Enemy.SKELETON_MAGE_WHITE, 200),
        (Enemy.SKELETON_MAGE_YELLOW, 300),
        (Enemy.SKELETON_MAGE_BLACK, 400),
        (Enemy.MUSHROOM_BLUE, 150),
        (Enemy.MUSHROOM_PURPLE, 300),
        (Enemy.GOLEM_LIGHT, 400),
        (Enemy.GOLEM_DARK, 600),
        (Enemy.ARMADILLO_WHITE, 300),
        (Enemy.ARMADILLO_YELLOW, 400),
        (Enemy.CLONE, 150),
        (Enemy.MOLE, 250),
        (Enemy.WIGHT, 350),
        (Enemy.MUSHROOM_EXPLODING, 150),
        (Enemy.SLIME_FIRE, 150),
        (Enemy.SLIME_ICE, 150),
        (Enemy.SKELETON_KNIGHT_WHITE, 300),
        (Enemy.SKELETON_KNIGHT_YELLOW, 400),
        (Enemy.SKELETON_KNIGHT_BLACK, 500),
        (Enemy.ELEMENTAL_FIRE, 300),
        (Enemy.ELEMENTAL_ICE, 300),
        (Enemy.GOBLIN_PURPLE, 300),
        (Enemy.GOBLIN_GRAY, 500),
        (Enemy.BEETLE_FIRE, 350),
        (Enemy.BEETLE_ICE, 350),
        (Enemy.HELLHOUND, 250),
        (Enemy.SHOVE_MONSTER_PURPLE, 250),
        (Enemy.YETI, 400),
        (Enemy.GHAST, 450),
        (Enemy.CAULDRON_MIMIC_FIRE, 100),
        (Enemy.CAULDRON_MIMIC_ICE, 100),
        (Enemy.SHOVE_MONSTER_GRAY, 350),
        (Enemy.GOBLIN_BOMBER, 300),
        (Enemy.BAT_BLACK, 350),
        (Enemy.ARMADILLO_ORANGE, 500),
        (Enemy.BLADEMASTER_APPRENTICE, 300),
        (Enemy.BLADEMASTER_MASTER, 400),
        (Enemy.GHOUL, 550),
        (Enemy.GOLEM_OOZE, 800),
        (Enemy.HARPY, 150),
        (Enemy.LICH_WHITE, 200),
        (Enemy.LICH_YELLOW, 300),
        (Enemy.LICH_BLACK, 400),
        (Enemy.MONKEY_GREEN, 150),
        (Enemy.PIXIE, 200),
        (Enemy.WARLOCK_BLUE, 150),
        (Enemy.WARLOCK_NEON, 250),
    ]
    BASE_COST = 200

    NTYPES = 6

    def __init__(self, floor):
        cap = 1000
        if floor == 0:
            cap = 150
        elif floor == 1:
            cap = 250

        eligible = []
        for entry in self.ELIGIBLE:
            type, cost = entry
            if cost <= cap:
                eligible.append(entry)

        self.pool = random.sample(eligible, self.NTYPES)

    def pick(self, n):
        cost = n * self.BASE_COST

        # This goes over-cost easily, but that should be OK.
        ret = []
        while cost > 0:
            et, ec = random.choice(self.pool)
            ret.append(et)
            cost -= ec
        return ret

class MinibossPool(object):
    def __init__(self):
        self.prev_miniboss = None

    def pick(self, floor):
        if floor == 0:
            miniboss_pool = [
                Enemy.DIREBAT_YELLOW,
                Enemy.DRAGON_GREEN,
                Enemy.MINOTAUR_LIGHT,
                ]
        elif floor == 1:
            miniboss_pool = [
                Enemy.DIREBAT_GRAY,
                Enemy.DRAGON_RED,
                Enemy.MINOTAUR_DARK
                ]
        else:
            miniboss_pool = [
                Enemy.DRAGON_RED,
                Enemy.MINOTAUR_DARK
                ]

        random.shuffle(miniboss_pool)

        while True:
            miniboss = miniboss_pool.pop()
            if miniboss != self.prev_miniboss:
                break
        self.prev_miniboss = miniboss

        return miniboss

class ItemPool(object):
    KIND_RED = 0
    KIND_PURPLE = 1
    KIND_BLACK = 2
    NKIND = 3

    # Certain items are intentionally omitted from the pool despite normally being available to Cadence
    # in the original game.
    #
    # These items:
    # - ring_peace -- does nothing except the +1 empty heart, because the levels are pre-generated
    # - ring_shadows -- no shops
    # - ring_charisma -- no shops
    # - ring_gold -- no shops
    # - ring_phasing -- not combat oriented

    # TODO: Put more items here, and account for item strength somehow.
    POOLS = {
        KIND_RED: [
            'food_1',
            'food_2',
            'food_3',
            'food_4',
            'holy_water',
            'bomb_3',
            'war_drum',
            'blood_drum',
            'hud_backpack',
            'holster',
            'torch_1',
            'torch_2',
            'torch_3',
            'torch_foresight',
            'torch_glass',
            'torch_infernal',
            'torch_obsidian',
        ],
        KIND_PURPLE: [
            'ring_courage',
            'ring_war',
            'ring_mana',
            'ring_might',
            'ring_luck',
            'ring_regeneration',
            'ring_protection',
            'ring_shielding',
            'ring_becoming',
            'spell_fireball',
            'spell_freeze_enemies',
            'spell_heal',
            'spell_bomb',
            'spell_shield',
            'spell_transmute',
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
