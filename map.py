__author__ = 'Unomi'
from tile import Tile


class Map:
    def __init__(self, width, length, height):
        self.__w = width
        self.__l = length
        self.__h = height
        self.__space = [None] * self.__l
        for i in range(self.__l):
            self.__space[i] = [None] * self.__w
            for j in range(self.__w):
                self.__space[i][j] = [Tile(None)] * self.__h

    def __str__(self):
        out = ''
        for i in range(self.__l):
            out += "\n"
            for j in range(self.__w):
                for k in range(self.__h):
                    out += str(self.__space[i][j][k])+str(k)+' '
        return out