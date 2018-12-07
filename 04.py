#!/usr/bin/python

# 2018-12-06 bob.p.wei@gmail.com

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
            self.sleep = 0
            self.schedule = {}

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
            guards[id_].sleep += entry.min - start

    sleepy_guard = None
    for k in guards:
        if not sleepy_guard:
            sleepy_guard = guards[k]
            next
        if guards[k].sleep > sleepy_guard.sleep:
            sleepy_guard = guards[k]
    print(f'[04a] sleepy_guard #{sleepy_guard.id_} slept {sleepy_guard.sleep} minutes!')
