#!/usr/bin/env python

# 2019-09-17 thehungryturnip@gmail.com

import hashlib
import sys
from collections import defaultdict, namedtuple
from enum import Enum, auto

Result = namedtuple('Result', ['min', 'state_hash', 'tree_count', 'yard_count'])

class Area:

    class Type(Enum):
        OPEN = auto()
        TREE = auto()
        YARD = auto()

    def __init__(self):
        self.__TYPE_TO_SYMBOL = {
                Area.Type.OPEN: '.',
                Area.Type.TREE: '|',
                Area.Type.YARD: '#',
                }

        self.__SYMBOL_TO_TYPE = {
                '.': Area.Type.OPEN,
                '|': Area.Type.TREE,
                '#': Area.Type.YARD,
                }
        self.__current = []
        self.__loop_start = None
        self.__loop_length = None
        self.__results_by_min = []
        self.__results_by_state_hash = defaultdict()

    def add_row(self, row_str):
        new_row = [self.__SYMBOL_TO_TYPE[c] for c in row_str]
        self.__current.append(new_row)

    def get_result_at(self, min_):
        while min_ >= len(self.__results_by_min) and not self.__loop_start:
            self.__process_round()
        if self.__loop_start:
            min_ = (min_ - self.__loop_start) % self.__loop_length
            min_ += self.__loop_start
        return self.__results_by_min[min_]
    
    def __process_round(self):
        self.__log_result()
        if self.__loop_start:
            return
        self.__past = [r.copy() for r in self.__current]
        for r in range(len(self.__past)):
            for c in range(len(self.__past[r])):
                past_type = self.__past[r][c]
                nearby = self.__get_nearby(r, c)
                if (past_type == Area.Type.OPEN 
                        and nearby[Area.Type.TREE] >= 3):
                    self.__current[r][c] = Area.Type.TREE
                if (past_type == Area.Type.TREE 
                        and nearby[Area.Type.YARD] >= 3):
                    self.__current[r][c] = Area.Type.YARD
                if past_type == Area.Type.YARD:
                    if not (nearby[Area.Type.TREE] > 0 
                            and nearby[Area.Type.YARD] > 0):
                        self.__current[r][c] = Area.Type.OPEN

    def __get_nearby(self, r, c):
        nearby = defaultdict(lambda: 0)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if not (dr == 0 and dc == 0):
                    if 0 <= (r + dr) < len(self.__past):
                        if 0 <= (c + dc) < len(self.__past[r + dr]):
                            nearby[self.__past[r + dr][c + dc]] += 1
        return nearby

    def __log_result(self):
        self.__check_state_for_loop()
        if self.__loop_start:
            return
        counts = defaultdict(lambda: 0)
        for r in self.__current:
            for c in r:
                counts[c] += 1
        min_ = len(self.__results_by_min)
        state_hash = hashlib.md5(str(self).encode()).digest()
        tree_count = counts[Area.Type.TREE]
        yard_count = counts[Area.Type.YARD]
        result = Result(min_, state_hash, tree_count, yard_count)
        self.__results_by_min.append(result)
        self.__results_by_state_hash[state_hash] = result

    def __check_state_for_loop(self):
        state_hash = hashlib.md5(str(self).encode()).digest()
        if state_hash in self.__results_by_state_hash:
            self.__loop_start = self.__results_by_state_hash[state_hash].min
            self.__loop_length = len(self.__results_by_min) - self.__loop_start

    def __str__(self):
        str_ = ''
        for r in self.__current:
            if not str_ == '':
                str_ += '\n'
            for c in r:
                str_ += self.__TYPE_TO_SYMBOL[c]
        return str_
    
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':

    PART_A_ROUNDS = 10
    PART_B_ROUNDS = 1000000000

    filename = sys.argv[1]
    print(f'filename: {filename}')

    a = Area()

    with open(filename, 'r') as f:
        for line in f:
            a.add_row(line.strip())

    r = a.get_result_at(PART_A_ROUNDS)
    print(f'[18a] There are {r.tree_count} trees and {r.yard_count} yards with'
          f' a resource value of {r.tree_count * r.yard_count} after'
          f' {PART_A_ROUNDS} minutes.')

    r = a.get_result_at(PART_B_ROUNDS)
    print(f'[18b] There are {r.tree_count} trees and {r.yard_count} yards with'
          f' a resource value of {r.tree_count * r.yard_count} after'
          f' {PART_B_ROUNDS} minutes.')
