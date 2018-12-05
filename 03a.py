#!/usr/bin/python

# 2018-12-05 thehungryturnip@gmail.com

import re
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')
    
    class Claim():
        
        def __init__(self, x, y, w, h):
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
        # for i in range(2):
            # print(line, end='')
            d = re.split(' |,|: |x|\n', line)
            c = Claim(int(d[2]), int(d[3]), int(d[4]), int(d[5]))
            claims.append(c)
            # print(c)
            line = file_.readline()
    # claims.append(Claim(0,0,2,3))
    # claims.append(Claim(0,0,1,5))
    # claims.append(Claim(0,0,5,1))

    fabric = {}
    for c in claims:
        # print(c)
        for h in range(c.h):
            for w in range(c.w):
                coord = f'{c.x + h}x{c.y + w}'
                # print(coord)
                if coord in fabric:
                    fabric[coord] += 1
                else:
                    fabric[coord] = 1

    overlaps = 0
    for k in fabric:
        if fabric[k] > 1:
            overlaps += 1

    print(f'overlaps: {overlaps}')
