#!/usr/bin/python

# 2018-12-04 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    twos = 0
    threes = 0
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            counts = {}
            for c in line:
                if c not in counts:
                    counts[c] = 1
                else:
                    counts[c] += 1
            if 2 in counts.values():
                twos += 1
            if 3 in counts.values():
                threes += 1
            line = file_.readline()

    print(f'{twos} * {threes} = {twos * threes}')
