#!/usr/bin/python

# 2018-12-04 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    ids = []
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            ids.append(line.rstrip())
            line = file_.readline()

    twos = 0
    threes = 0
    for id_ in ids:
        counts = {}
        for c in id_:
            if c not in counts:
                counts[c] = 1
            else:
                counts[c] += 1
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    print(f'[02a] {twos} * {threes} = {twos * threes}')

    for i in range(len(ids) - 1):
        for j in range(i + 1, len(ids)):
            if not len(ids[i]) == len(ids[j]):
                next
            for k in range(len(ids[i])):
                if ids[i][:k] + ids[i][k + 1:] == ids[j][:k] + ids[j][k + 1:]:
                    print(f'[02b] {ids[i]}')
                    print(f'[02b] {ids[j]}')
                    print(f'[02b] {ids[i][k]} vs {ids[j][k]} at {k}')
