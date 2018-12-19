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
                next_gen = next_gen_lstrip.rstrip(NO_PLANT)
                self.pots = next_gen

        def garden_index(self):
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

    curr_index = g.garden_index()
    print(f'0:{g}:{curr_index}')
    i = 0
    while i < generation_count:
        g.progress(reach, 1)
        prev_index = curr_index
        curr_index = g.garden_index()
        print(f'{i + 1}:{g}:{curr_index}:{curr_index - prev_index}')
        i += 1

    print(f'[12a] the plant index is {g.garden_index()}' +
          f' after {generation_count} generations.')

    # noticed that the general layout of the garden stabilizes with:
    stable_garden = '#..#.##...#.##....#....#.##...#.....#.##...#.##...#.##...#.##...#..#.##...#.##...#.##...#.##...#.##...#.##...#.##...#.##...#.##...#.##...#.##'

    # thus look for first generation with stable_garden
    while not g.pots == stable_garden:
        g.progress(reach, 1)
        prev_index = curr_index
        curr_index = g.garden_index()
        print(f'{i + 1}:{g}:{curr_index}:{curr_index - prev_index}')
        i += 1
    
    # progress 10 more to determine delta and confirm pattern
    for j in range(10):
        g.progress(reach, 1)
        prev_index = curr_index
        curr_index = g.garden_index()
        print(f'{i + 1}:{g}:{curr_index}:{curr_index - prev_index}')
        i += 1

    # at generation #122 and index 8990, the pattern starts to repeat with a delta of 58, thus
    print(f'[12b] the plant index at generattion 50000000000 is:' +
          f' {8990 + (50000000000 - 122 - 1) * 58}')
