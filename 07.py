#!/usr/bin/python

# 2018-12-10 thehungryturnip@gmail.com

import sys
from heapq import heapify, heappush, heappop

if __name__ == '__main__':
    
    class Step:

        def __init__(self, name):
            self.name = name
            self.before = 0
            self.after = []

        def __lt__(self, other):
            return self.name < other.name

        def __str__(self):
            return f'{self.name}:{self.before}:{[a.name for a in self.after]}'

        def __repr__(self):
            return self.__str__()

    filename = sys.argv[1]
    print(f'file: {filename}')

    with open(filename, 'r') as f:
        reqs = f.readlines()
    reqs = [l.split() for l in reqs]
    reqs = [(l[1], l[7]) for l in reqs]

    steps = {}
    for b, a in reqs:
        if b not in steps:
            steps[b] = Step(b)
        before = steps[b]
        if a not in steps:
            steps[a] = Step(a)
        after = steps[a]
        before.after.append(after)
        after.before += 1
    print(steps)
    
    workflow = ''
    active_steps = [s for s in steps.values() if s.before == 0]
    heapify(active_steps)
    while active_steps:
        s = heappop(active_steps)
        workflow += s.name
        for a in s.after:
            a.before -= 1
            if a.before == 0:
                heappush(active_steps, a)
    print(f'[07a] workflow should be: {workflow}')
