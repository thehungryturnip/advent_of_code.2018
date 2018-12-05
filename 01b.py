#!/usr/bin/python

# 2018-12-04 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    deltas = []
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            deltas.append(int(line))
            line = file_.readline()

    sum_ = 0
    seen = {}
    next_ = 0
    # assumes that <sum_> *will* eventually be in <seen>
    while sum_ not in seen: 
        seen[sum_] = 1
        sum_ += deltas[next_]
        next_ += 1
        if next_ == len(deltas):
            next_ = 0

    print(f'duplicate sum: {sum_}')
