#!/usr/bin/python

# 2018-12-10 thehungryturnip@gmail.com

import sys
from heapq import heapify, heappush, heappop

if __name__ == '__main__':

    WORKER_COUNT = 5
    
    class Step:

        def __init__(self, name):
            self.name = name
            self.before = 0
            self.after = []
            self.length = 60
            self.done = None

        def __lt__(self, other):
            return self.name < other.name

        def __str__(self):
            return f'{self.name}:{self.before}:{"".join(sorted([a.name for a in self.after]))}'

        def __repr__(self):
            return self.__str__()

    def create_steps(reqs):
        steps = {}
        for b, a in reqs:
            if b not in steps:
                steps[b] = Step(b)
                steps[b].length += ord(b) - ord('A') + 1
            before = steps[b]
            if a not in steps:
                steps[a] = Step(a)
                steps[a].length += ord(a) - ord('A') + 1
            after = steps[a]
            before.after.append(after)
            after.before += 1
        return steps

    filename = sys.argv[1]
    print(f'file: {filename}')

    with open(filename, 'r') as f:
        reqs = f.readlines()
    reqs = [l.split() for l in reqs]
    reqs = [(l[1], l[7]) for l in reqs]

    steps = create_steps(reqs)
    # print(sorted(list(steps.values())))
    
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

    todos = create_steps(reqs)
    available = [s for s in todos.values() if s.before == 0]
    heapify(available)
    doing = []
    time = 0
    while doing or available:
        while available and len(doing) < WORKER_COUNT:
            s = heappop(available)
            s.done = time + s.length
            # print(f'worker #{len(doing)} starting {s.name} from {time} to {s.done}')
            heappush(doing, (s.done, s))
        s = heappop(doing)[1]
        time = s.done
        for a in s.after:
            a.before -= 1
            if a.before == 0:
                heappush(available, a)
    print(f'[07b] work can be done in {time} min with {WORKER_COUNT} workers.')
