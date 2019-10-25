#!/usr/bin/env python3

#
# thehungryturnip@gmail.com
#
# Advent of Code 2018. Day 22.
#

import sys
from collections import namedtuple, defaultdict
from enum import Enum, auto
from heapq import heappush, heappop

X_GEO_MULTIPLIER = 16807
Y_GEO_MULTIPLIER = 48271
EROSION_MODULUS = 20183
TAVERSE_TIME = 1
TOOL_CHANGE_TIME = 7

class Direction(Enum):
    RIGHT = auto()
    BELOW = auto()
    LEFT = auto()
    ABOVE = auto()

class Coord(namedtuple('Coord', ['x', 'y'])):
    def neighbor(self, d):
        return {
                Direction.RIGHT: self + Coord(1, 0),
                Direction.BELOW: self + Coord(0, 1),
                Direction.LEFT: self + Coord(-1, 0),
                Direction.ABOVE: self + Coord(0, -1)
                }[d]

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

class Symbol(Enum):
    MOUTH = 'M'
    TARGET = 'T'
    ROCKY = '.'
    WET = '='
    NARROW = '|'

class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

class Tool(Enum):
    NONE = 0
    TORCH = 1
    CLIMBING = 2
    
    def use_for(self, type_):
        if type_ == Type.ROCKY:
            return self in (Tool.CLIMBING, Tool.TORCH)
        if type_ == Type.WET:
            return self in (Tool.CLIMBING, Tool.NONE)
        if type_ == Type.NARROW:
            return self in (Tool.TORCH, Tool.NONE)

class State(namedtuple('State', ['coord', 'tool'])):
    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y

    def __str__(self):
        return f'({self.coord.x},{self.coord.y}){self.tool.name}'

class Record(namedtuple('Record', ['state', 'time'])):

    TIME_TOOL_CHANGE = 7
    TIME_MOVE = 1

    @property
    def coord(self):
        return self.state.coord

    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y

    @property
    def tool(self):
        return self.state.tool

    def change_tool(self, tool):
        time = self.time
        if not tool == self.state.tool:
            time += self.TIME_TOOL_CHANGE
        return Record(State(Coord(self.x, self.y), tool), time)

    def change_towards(self, direction):
        coord = self.state.coord.neighbor(direction)
        return Record(State(coord, self.tool), self.time + 1)

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __le__(self, other):
        return self.time <= other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __str__(self):
        return (f'({self.state.coord.x},{self.state.coord.y})'
                f'{self.state.tool.name}:{self.time}')

class Cave:
    def __init__(self, depth, target):
        self.mouth = Coord(0, 0)
        self.target = target
        self.depth = depth
        self.erosion = {}
        self.records = {}

    def erosion_at(self, coord):
        if not coord in self.erosion:
            if coord == self.mouth or coord == self.target:
                geo_index = 0
            elif coord.y == 0:
                geo_index = coord.x * X_GEO_MULTIPLIER
            elif coord.x == 0:
                geo_index = coord.y * Y_GEO_MULTIPLIER
            else:
                left_coord = coord.neighbor(Direction.LEFT)
                left_erosion = self.erosion_at(left_coord)
                above_coord = coord.neighbor(Direction.ABOVE)
                above_erosion = self.erosion_at(above_coord)
                geo_index = left_erosion * above_erosion
            self.erosion[coord] = (geo_index + self.depth) % EROSION_MODULUS
        return self.erosion[coord]

    def type_at(self, coord):
        erosion = self.erosion_at(coord)
        return Type(erosion % len(Type))

    def symbol_at(self, coord):
        if coord == self.mouth:
            return Symbol.MOUTH.value
        if coord == self.target:
            return Symbol.TARGET.value
        t = self.type_at(coord)
        if t == Type.ROCKY:
            return Symbol.ROCKY.value
        if t == Type.WET:
            return Symbol.WET.value
        if t == Type.NARROW:
            return Symbol.NARROW.value

    def risk_to_target(self):
        risk = 0
        for x in range(self.target.x + 1):
            for y in range(self.target.y + 1):
                c = Coord(x, y)
                if not c == self.mouth and not c == self.target:
                    risk += self.type_at(c).value
        return risk

    def time_to_target(self):
        target_state = State(self.target, Tool.TORCH)
        mouth_state = State(self.mouth, Tool.TORCH)
        self.records[mouth_state] = 0
        exploring = [Record(mouth_state, 0)]
        while exploring:
            record = heappop(exploring)
            # print(f'pop: {record}')
            new_records = self.explore(record)
            for r in new_records:
                if (not r.state in self.records or 
                        r.time < self.records[r.state]):
                    self.records[r.state] = r.time
                    heappush(exploring, r)
            # if self.records.get(State(Coord(2, 2), Tool.TORCH)):
                # return None
            if target_state in self.records:
                return self.records[target_state]
        return None

    def explore(self, record):
        new_records = []
        for d in Direction:
            coord = record.coord.neighbor(d)
            if coord.x < 0 or coord.y < 0:
                continue
            type_ = self.type_at(coord)
            for t in Tool:
                if t.use_for(type_):
                    new_record = record.change_towards(d)
                    if not t == record.tool:
                        new_record = new_record.change_tool(t)
                    new_records.append(new_record)
        return new_records

    def __str__(self):
        r_x = range(self.target.x + 1)
        r_y = range(self.target.y + 1)
        symbols = [[self.symbol_at(Coord(x, y)) for x in r_x] for y in r_y]
        return '\n'.join([''.join(row) for row in symbols])

filename = sys.argv[1]
print(f'filename: {filename}')

with open(filename, 'r') as f:
    lines = f.read().split('\n')

for l in lines:
    l = l.split()
    if len(l) > 1:
        if l[0] == 'depth:':
            depth = int(l[1])
            print(f'depth:{depth}')
        if l[0] == 'target:':
            target = l[1]
            print(f'target:{target}')
        
target = target.split(',')

c = Cave(depth, Coord(int(target[0]), int(target[1])))
print(f'[22a] Risk to get to target is {c.risk_to_target()}.')
print(f'[22b] Shortest time to get to target is {c.time_to_target()}.')
