#!/usr/bin/python

# 2019-06-12 thehungryturnip@gmail.com

import re
import sys
from collections import namedtuple
from enum import IntEnum, auto

class Coord(namedtuple('Coord', ['x', 'y'])):

    def topleft(self):
        return self + Coord(-1, -1)

    def top(self):
        return self + Coord(0, -1)

    def topright(self):
        return self + Coord(1, -1)

    def left(self):
        return self + Coord(-1, 0)

    def right(self):
        return self + Coord(1, 0)

    def bottomleft(self):
        return self + Coord(-1, 1)

    def bottom(self):
        return self + Coord(0, 1)

    def bottomright(self):
        return self + Coord(1, 1)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return self.__str__()

class Vein(dict):

    __DEF_DELIM = '=|, '
    __RANGE_DELIM = '..'

    def __init__(self, argstr):
        args = re.split(Vein.__DEF_DELIM, argstr)
        self[args[0]] = Vein.__expand(args[1])
        self[args[2]] = Vein.__expand(args[3])

    def get_coords(self):
        return [Coord(x, y) for x in self['x'] for y in self['y']]

    def __expand(val):
        val = val.split(Vein.__RANGE_DELIM)
        val = map(lambda i: int(i), val)
        val = list(val)
        if len(val) == 1:
            return [val[0]]
        vals = []
        for i in range(val[0], val[1] + 1):
            vals.append(i)
        return vals

class Scan(dict):

    __COORD_WATER_SOURCE = Coord(500, 0)

    class Type(IntEnum):
        CLAY = auto()
        WATER_SETTLED = auto()
        WATER_FLOWING = auto()

    def __init__(self):
        self.__TYPE_TO_SYMBOL = {
                Scan.Type.CLAY: '#',
                Scan.Type.WATER_SETTLED: '~',
                Scan.Type.WATER_FLOWING: '|',
                None: '.',
                }

    def add_vein(self, v):
        coords = v.get_coords()
        for c in coords:
            self[c] = Scan.Type.CLAY
            self.__check_minmax(c)

    def analyze_flow(self):
        c = Scan.__COORD_WATER_SOURCE
        if not self.get(c):
            self[c] = Scan.Type.WATER_FLOWING
            analyzing = [c.left(), c.right(), c.bottom()]
            while analyzing:
                analyzing.extend(self.__analyze(analyzing.pop()))

    def count_wet(self):
        # -1 to remove the source
        return len([v for v in s.values() if v > Scan.Type.CLAY]) - 1

    def __check_minmax(self, c):
        if not hasattr(self, 'x_min') or c.x - 1 < self.x_min:
            self.x_min = c.x - 1
        if not hasattr(self, 'x_max') or c.x + 1 > self.x_max:
            self.x_max = c.x + 1
        if not hasattr(self, 'y_max') or c.y > self.y_max:
            self.y_max = c.y

    def __analyze(self, c):
        to_analyze = []

        if not self.get(c):
            # flow down
            if c.y <= self.y_max and self.__is_water(c.top()):
                self[c] = Scan.Type.WATER_FLOWING
                to_analyze.extend([c.left(), c.right(), c.bottom()])

            # flow left
            if (self.get(c.right()) == Scan.Type.WATER_FLOWING and 
                    self.__is_settled(c.bottomright())):
                self[c] = Scan.Type.WATER_FLOWING
                to_analyze.extend([c.left(), c.bottom()])

            # flow right
            if (self.get(c.left()) == Scan.Type.WATER_FLOWING and
                    self.__is_settled(c.bottomleft())):
                self[c] = Scan.Type.WATER_FLOWING
                to_analyze.extend([c.right(), c.bottom()])
        
        # check to see if it needs to settle
        if (self.get(c) == Scan.Type.WATER_FLOWING and
                self.__is_settled(c.bottom())):
            l = -1
            while self.__is_water(c + Coord(l, 0)):
                l -= 1
            r = 1
            while self.__is_water(c + Coord(r, 0)):
                r += 1
            if (self.get(c + Coord(l, 0)) == self.get(c + Coord(r, 0))
                    == Scan.Type.CLAY):
                self[c] = Scan.Type.WATER_SETTLED
                to_analyze.extend([c.top(), c.left(), c.right()])

        return to_analyze

    def __is_settled(self, c):
        t = self.get(c)
        return t == Scan.Type.WATER_SETTLED or t == Scan.Type.CLAY

    def __is_water(self, c):
        t = self.get(c)
        return t == Scan.Type.WATER_FLOWING or t == Scan.Type.WATER_SETTLED

    def __str_y(self, y):
        row = ""
        for x in range(self.x_min, self.x_max + 1):
            t = self.get(Coord(x, y))
            row += self.__TYPE_TO_SYMBOL[t]
        return row

    def __str__(self):
        return '\n'.join([self.__str_y(y) for y in range(self.y_max + 1)])

if __name__ == '__main__':

    filename = sys.argv[1]
    print(f'filename: {filename}')

    s = Scan()

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                v = Vein(line)
                s.add_vein(v)
    s.analyze_flow()
    print(s)
    print(f'[17a] {s.count_wet()} number of tiles are reachable by water.')
