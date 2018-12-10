#!/usr/bin/python

# 2018-12-09 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':

    class Area():

        def __init__(self, index, x, y):
            self.index = index
            self.x = x
            self.y = y
            self.size = 0
            self.edge = False

        def __str__(self):
            return f'{self.index}:({self.x},{self.y}):{self.size}:{self.edge}'

        def __repr__(self):
            return self.__str__()

    class Map():

        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.map = [['-' for i in range(self.h)] for i in range(self.w)]
    
        def __getitem__(self, key):
            return self.map[key[0] - self.x][key[1] - self.y]

        def __setitem__(self, key, val):
            x = key[0] - self.x
            y = key[1] - self.y
            self.map[x][y] = val

        def __str__(self):
            string = ''
            for i in range(self.h):
                for j in range(self.w):
                    if not j == 0:
                        string += ' '
                    string += str(self.map[j][i])
                string += '\n'
            return string

        def __repr__(self):
            return self.__str__()

    def create_areas(filename):
        areas = []
        with open(filename, 'r') as f:
            line = f.readline()
            index = 0
            while line:
                line = line.split(',')
                areas.append(Area(index, int(line[0]), int(line[1])))
                line = f.readline()
                index += 1
        return areas

    def distance_between(x1, y1, x2, y2):
        return abs(x2 - x1) + abs(y2 - y1)

    def analyze_areas(areas):
        left = min([o.x for o in areas])
        right = max([o.x for o in areas])
        top = min([o.y for o in areas])
        bot = max([o.y for o in areas])

        map_ = Map(left, top, right - left + 1, bot - top + 1)
        # print(map_)

        for x in range(left, right + 1):
            for y in range(top, bot + 1):
                closest = areas[0]
                min_distance = distance_between(x, y, closest.x, closest.y)
                for a in areas[1:]:
                    distance = distance_between(x, y, a.x, a.y)
                    if distance == min_distance:
                        closest = None
                        continue
                    if distance < min_distance:
                        closest = a
                        min_distance = distance
                if closest:
                    map_[(x, y)] = closest.index
                    closest.size += 1
                    if x == left or x == right or y == top or y == bot:
                        closest.edge = True
        return map_

    def find_biggest_not_edge(areas):
        biggest = None
        for a in areas:
            if not a.edge:
                if not biggest:
                    biggest = a
                    continue
                if a.size > biggest.size:
                    biggest = a
        return biggest

    filename = sys.argv[1]
    print(f'file: {filename}')

    areas = create_areas(filename)
    # print(areas)

    map_ = analyze_areas(areas)
    # print(areas)
    # print(map_)

    biggest = find_biggest_not_edge(areas)
    print(f'[06a] biggest none-infinite area has size: {biggest.size}')
