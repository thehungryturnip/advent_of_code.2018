#!/usr/bin/env python3

#
# thehungryturnip@gmail.com
#
# Day 20 of the Advent of Code 2018
#

import re
import sys
from collections import namedtuple
from enum import Enum, auto
from networkx import Graph, algorithms

class Direction(Enum):
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'
    NORTH = 'N'

class Coord(namedtuple('Coord', ['x', 'y'])):
    def delta(self, dir_):
        delta = DIRECTION_DELTAS[dir_]
        return Coord(self.x + delta.x, self.y + delta.y)

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return self.__str__()

DIRECTION_DELTAS = {
        Direction.EAST: Coord(1, 0),
        Direction.SOUTH: Coord(0, 1),
        Direction.WEST: Coord(-1, 0),
        Direction.NORTH: Coord(0, -1),
        }

class Instruction(Enum):
    START = '^'
    END = '$'
    STEP = 'ESWN'
    START_BRANCHING = '('
    NEW_BRANCH = '|'
    END_BRANCHING = ')'

class Split:
    def __init__(self, branches):
        self.prev = branches
        self.next = set()

class Map(Graph):

    DEFSTR_REGEX = '\^.*\$'

    def __init__(self, defstr):
        super().__init__()
        self.defstring = defstr
        self.build_graph()
        self.lengths = algorithms.shortest_path_length(self, Coord(0, 0))

    def build_graph(self):
        for c in self.defstring:
            if c is Instruction.START.value:
                self.clear()
                branches = set([Coord(0, 0)])
                splits = []
            elif c in Instruction.STEP.value:
                new_branches = set()
                for curr_node in branches:
                    next_node = curr_node.delta(Direction(c))
                    self.add_edge(curr_node, next_node)
                    new_branches.add(next_node)
                branches = new_branches
            elif c in Instruction.START_BRANCHING.value:
                splits.append(Split(branches))
            elif c in Instruction.NEW_BRANCH.value:
                splits[-1].next = splits[-1].next.union(branches)
                branches = splits[-1].prev
            elif c in Instruction.END_BRANCHING.value:
                branches = branches.union(splits.pop().next)

    def furthest_distance(self):
        return max(self.lengths.values())

    def distance_over(self, length):
        return len([v for v in self.lengths.values() if v >= 1000])

    def __str__(self):
        return f'nodes:{len(self.nodes)} edges:{len(self.edges)}\n{self.edges}'

if __name__ == '__main__':
    COMMENT_CHAR = '#'

    filename = sys.argv[1]
    print(f'filename: {filename}')

    defstrs = []
    with open(filename, 'r') as f:
        for l in [l.strip() for l in f.readlines()]:
            if not l[0] == COMMENT_CHAR:
                defstrs += re.findall(Map.DEFSTR_REGEX, l)

    maps = []
    for d in defstrs:
        m = Map(d)
        maps.append(m)

    for m in maps:
        print(m.defstring)
        print(f'[20a] Furthest room is {m.furthest_distance()} away.')
        print(f'[20b] {m.distance_over(1000)} rooms 1000 or more doors away.')
