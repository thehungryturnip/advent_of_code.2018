#!/usr/bin/python

# 2018-12-05 thehungryturnip@gmail.com

import re
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')
    
    class Claim():
        
        def __init__(self, id_, x, y, w, h):
            self.id_ = id_
            self.x = x
            self.y = y
            self.w = w
            self.h = h

        def __str__(self):
            return f'({self.x},{self.y}){self.w}x{self.h}'

    claims = []
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            d = re.split('#| |,|: |x|\n', line)
            c = Claim(int(d[1]), int(d[3]), int(d[4]), int(d[5]), int(d[6]))
            claims.append(c)
            line = file_.readline()

    fabric = {}
    for c in claims:
        for h in range(c.h):
            for w in range(c.w):
                coord = f'{c.x + w}x{c.y + h}'
                if coord in fabric:
                    fabric[coord] += 1
                else:
                    fabric[coord] = 1

    overlaps = 0
    for k in fabric:
        if fabric[k] > 1:
            overlaps += 1
    print(f'overlaps: {overlaps}')

    for c in claims:
        overlap = False
        for h in range(c.h):
            for w in range(c.w):
                coord = f'{c.x + w}x{c.y + h}'
                if fabric[coord] > 1:
                    overlap = True
        if not overlap:
            print(f'no overlap: {c.id_}')
