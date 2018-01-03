__author__ = 'Unomi'


class Char:
    def __init__(self):
        self.__weapon = None

        self.__stats = {
            'max_health': 100,
            'health': 100,
            'strength': 10,
            'agility': 10,
            'intelligence': 10,
            'mana': 100
        }

    def get_max_mana(self):
        return self.__stats['intelligence']*0.1