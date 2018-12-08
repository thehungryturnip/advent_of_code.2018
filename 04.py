#!/usr/bin/python

# 2018-12-06 thehungryturnip@gmail.com

import re
import sys

from enum import Enum

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    class LogEntry():

        EventType = Enum('EventType', 'SHIFT SLEEP WAKE')

        EVENT_TYPE_TEXT = {
                'Guard': EventType.SHIFT,
                'falls': EventType.SLEEP,
                'wakes': EventType.WAKE
                }

        def __init__(self, text):
            data = re.split('\[|-| #|:|] | |\n', text)
            self.min = int(data[5])
            self.type = self.EVENT_TYPE_TEXT[data[6]]
            if self.type == LogEntry.EventType.SHIFT:
                self.guard = int(data[7])

    class Guard():

        def __init__(self, id_):
            self.id_ = id_
            self.sleep_schedule = {}

        def add_sleep(self, from_, to):
            for i in range(from_, to):
                if i not in self.sleep_schedule:
                    self.sleep_schedule[i] = 1
                    continue
                self.sleep_schedule[i] += 1

        def __str__(self):
            return f'#{self.id_}:\n{self.sleep_schedule}'

    lines = []
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            lines.append(line.strip())
            line = file_.readline()
    lines.sort()
    lines.reverse()

    guards = {}
    id_ = None
    start = 0
    while lines:
        line = lines.pop()
        entry = LogEntry(line)
        if entry.type == LogEntry.EventType.SHIFT:
            id_ = entry.guard
            if not id_ in guards:
                guards[id_] = Guard(id_)
        if entry.type == LogEntry.EventType.SLEEP:
            start = entry.min
        if entry.type == LogEntry.EventType.WAKE:
            guards[id_].add_sleep(start, entry.min)

    sleepy_guard = None
    for g in guards.values():
        if not sleepy_guard:
            sleepy_guard = g
            continue
        if (sum(g.sleep_schedule.values()) > 
            sum(sleepy_guard.sleep_schedule.values())):
            sleepy_guard = g

    sleepy_min = None
    for k in sleepy_guard.sleep_schedule:
        if not sleepy_min:
            sleepy_min = k
            continue
        if (sleepy_guard.sleep_schedule[k] > 
            sleepy_guard.sleep_schedule[sleepy_min]):
            sleepy_min = k
    print(f'[04a] sleepy_guard #{sleepy_guard.id_}' +
          f' slept for {sum(sleepy_guard.sleep_schedule.values())} minutes' +
          f' and is most sleepy at {sleepy_min}!' +
          f' {sleepy_guard.id_}x{sleepy_min}={sleepy_guard.id_ * sleepy_min}')

    sleepy_guard = None
    sleepy_min = None
    for g in guards.values():
        if not sleepy_guard:
            sleepy_guard = g
        for m in g.sleep_schedule:
            if not sleepy_min:
                sleepy_min = m
                continue
            if g.sleep_schedule[m] > sleepy_guard.sleep_schedule[sleepy_min]:
                sleepy_guard = g
                sleepy_min = m
    print(f'[04b] sleepy_guard #{sleepy_guard.id_}' +
          f' slept for a total of {sleepy_guard.sleep_schedule[sleepy_min]} minutes' +
          f' at {sleepy_min}!' +
          f' {sleepy_guard.id_}x{sleepy_min}={sleepy_guard.id_ * sleepy_min}')
