#!/usr/bin/python

# 2019-06-12 thehungryturnip@gmail.com

import sys
from collections import namedtuple

if __name__ == '__main__':

    Coord = namedtuple('Coord', ['x', 'y'])

    class Vein:
        pass

    filename = sys.argv[1]
    print(f'filename: {filename}')

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()
