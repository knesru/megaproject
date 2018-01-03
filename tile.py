__author__ = 'Unomi'
from item import Item
from char import Char


class Tile:
    def __init__(self, content):
        self.__chars = list()
        self.__items = list()
        self.__ores = list()
        if content is not None:
            for obj in content:
                if isinstance(obj, Item):
                    self.__items.append(obj)
                if isinstance(obj, Char):
                    self.__chars.append(obj)

    def __str__(self):
        return 'X'