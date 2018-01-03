__author__ = 'Unomi'

import math

materials = {
    'copper': {
        'density': 8.7,
        'durability': 1,
        'gems': 1,
        'toughness': 1,
    },
    'iron': {
        'density': 7.9,
        'durability': 3,
        'gems': 2,
        'toughness': 4,
    },
    'silver': {
        'density': 10.5,
        'durability': 2,
        'gems': 3,
        'toughness': 3,
    },
    'gold': {
        'density': 19.3,
        'durability': 4,
        'gems': 4,
        'toughness': 3,
    },
    'platinum': {
        'density': 21.5,
        'durability': 4,
        'gems': 5,
        'toughness': 3,
    },
    'mithril': {
        'density': 2.3,
        'durability': 6,
        'gems': 6,
        'toughness': 6,
    },
    'adamantium': {
        'density': 12.9,
        'durability': 10,
        'gems': 7,
        'toughness': 8,
    },
}

modifiers = {
    'worn': {
        'gems': ['-', 3, 'abs'],
        'durability': ['-', 10, '%'],
        'damage': ['-', 20, '%']
    },
    'general': {

    },
    'inlaid': {
        'gems': ['+', 2, 'abs'],
        'durability': ['-', 5, '%']
    },
    'omni': {
        'gems': ['+', 1, 'abs'],
        'durability': ['+', 20, '%'],
        'damage': ['+', 2, '%']
    },
    'super': {
        'gems': ['+', 1, 'abs'],
        'durability': ['+', 15, '%'],
        'damage': ['+', 2, 'abs']
    },
}

weapon_types = {
    'dagger': {
        'amount': 2,
        'basic_damage': 2,
        'range': 5,
        'defence': 0
    },
    'sword': {
        'amount': 4,
        'basic_damage': 6,
        'range': 7,
        'defence': 2
    },
    'longsword': {
        'amount': 7,
        'basic_damage': 13,
        'range': 10,
        'defence': 3,
    },
    'axe': {
        'amount': 15,
        'basic_damage': 16,
        'range': 9,
        'defence': 3
    },
}

armor_types = {
    'helmet': {
        'amount': 5,
        'basic_defence': 2
    },
    'waist': {
        'amount': 13,
        'basic_defence': 5
    },
    'greaves': {
        'amount': 9,
        'basic_defence': 3
    },
}

gems = {
    'amethyst': {
        'damage': ['+', 5, '%'],
    },
    'topaz': {
        'weight': ['-', 10, '%'],
    },
    'ruby': {
        'defence': ['+', 5, '%'],
    },
    'diamond': {
        'durability': ['+', 5, '%'],
    },
    'emerald': {
        'crit': ['+', 5, '%'],
    },
}


def apply_modifier(modifier, value):
    mod_value = modifier[1]
    if modifier[2] == '%':
        if modifier[0] == '+':
            return value * (1 + mod_value / 100)
        elif modifier[0] == '-':
            return value * (1 - mod_value / 100)
    elif modifier[2] == 'abs':
        if modifier[0] == '+':
            return value + mod_value
        elif modifier[0] == '-':
            return value - mod_value


class Wpn:
    def __init__(self, name, prop, w_prop, m_prop, gems):
        self.name = name
        self.set_stats(prop, w_prop, m_prop)
        self.gems = list()
        for gem_name in gems:
            self.append_gem(gem_name)

    def set_stats(self, prop, w_prop, m_prop):
        weight = w_prop['amount'] * prop['density'] / 50
        damage = w_prop['basic_damage'] * (1 + (prop['toughness'] - 1) / 10)
        damage = apply_modifier(m_prop.get('damage', ['+', 0, 'abs']), damage)
        self.weight = weight
        self.damage = damage
        self.range = w_prop['range']
        self.crit = 1
        self.durability = prop['durability']
        self.defence = w_prop['defence']

    def get_dps(self, strength=100):
        distance = self.range / 2
        t = math.sqrt(2 * distance * self.weight / strength)
        if t < 0.2:
            t = 0.2
        return self.damage / t

    def __gt__(self, other):
        return self.get_dps() > other.get_dps()

    def __str__(self):
        return str(self.name) + ' ' + str(self.damage) + ' ' + str(self.get_dps()) + ' ' + ','.join(self.gems)

    def append_gem(self, gem_name):
        self.gems.append(gem_name)
        for modifier_name in gems[gem_name].keys():
            if modifier_name == 'damage':
                self.damage = apply_modifier(gems[gem_name][modifier_name], self.damage)
            elif modifier_name == 'weight':
                self.weight = apply_modifier(gems[gem_name][modifier_name], self.weight)
            elif modifier_name == 'defence':
                self.defence = apply_modifier(gems[gem_name][modifier_name], self.defence)
            elif modifier_name == 'durability':
                self.durability = apply_modifier(gems[gem_name][modifier_name], self.durability)
            elif modifier_name == 'crit':
                self.crit = apply_modifier(gems[gem_name][modifier_name], self.crit)


def gem_generator(amount, start='amethyst'):
    if amount == 0:
        yield []
    else:
        keys = list(gems.keys())
        started = False
        keys.sort()
        for gem_name in keys:
            if gem_name == start:
                started = True

            if started:
                for gem_combinations in gem_generator(amount - 1, gem_name):
                    yield [gem_name] + gem_combinations


wpns = list()

for name, w_prop in weapon_types.items():
    for mat, prop in materials.items():
        for mod, m_prop in modifiers.items():
            gems_amount = prop['gems']
            if m_prop.get('gems'):
                gems_amount = apply_modifier(m_prop.get('gems'), gems_amount)
            if gems_amount < 0:
                gems_amount = 0
            for current_gem_set in gem_generator(gems_amount):
                wpns.append(Wpn(mod + ' ' + mat + ' ' + name, prop, w_prop, m_prop, current_gem_set))

wpns_sorted = sorted(wpns)

for w in wpns_sorted:
    print(w)

print(len(wpns_sorted))