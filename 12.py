#!/usr/bin/python

# 2018-12-13 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')
    generation_count = int(sys.argv[2])
    print(f'generation_count: = {generation_count}')
    
    HAS_PLANT = '#'
    NO_PLANT = '.'

    class Garden:

        def __init__(self):
            self.pots = ''
            self.zero = 0
            self.rules = {}

        def add_pots(self, pots):
            self.pots += pots
        
        def set_zero(self, zero):
            self.zero = zero

        def add_rule(self, condition, result):
            self.rules[condition] = result

        def progress(self, reach=0, generations=1):
            padding = NO_PLANT * (reach * 2 + 1)
            for g in range(generations):
                curr_gen = padding + self.pots + padding
                next_gen = ''
                for p in range(reach, len(curr_gen) - reach):
                    condition = curr_gen[p - reach:p + reach + 1]
                    next_gen += self.rules.get(condition, NO_PLANT)
                next_gen_lstrip = next_gen.lstrip(NO_PLANT)
                self.zero += len(next_gen) - len(next_gen_lstrip) - (reach + 1)
                self.pots = next_gen_lstrip.rstrip(NO_PLANT)

        def plant_index(self):
            total = 0
            for i in range(len(self.pots)):
                if self.pots[i] == HAS_PLANT:
                    total += i + self.zero
            return total

        def __str__(self):
            return self.pots

        def __repr__(self):
            return self.__str__()

    g = Garden()
    with open(filename, 'r') as f:
        initial_pots = None
        line = f.readline()
        while line:
            line = line.split()
            if line:
                if not initial_pots:
                    initial_pots = line[2]
                    g.add_pots(initial_pots)
                else:
                    condition = line[0]
                    reach = len(condition) // 2
                    result = line[2]
                    g.add_rule(condition, result)
            line = f.readline()

    print(f'0:{g}')
    for i in range(generation_count):
        g.progress(reach, 1)
        print(f'{i + 1}:{g}')

    print(f'[12a] the plant index is {g.plant_index()}' +
          f' after {generation_count} generations.')
