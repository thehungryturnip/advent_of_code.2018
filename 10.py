#!/usr/bin/python

# 2018-12-11 thehungryturnip@gmail.com

import re
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    class Point:
        def __init__(self, x, y, dx, dy):
            self.x = int(x)
            self.y = int(y)
            self.dx = int(dx)
            self.dy = int(dy)

        def move(self, steps):
            steps = int(steps)
            self.x += steps * self.dx
            self.y += steps * self.dy

        def __str__(self):
            return f'{self.x},{self.y}:{self.dx},{self.dy}'

        def __repr__(self):
            return self.__str__()

    class Canvas:

        BLANK_CANVAS = ' '
        BRUSH_STROKE = '#'

        def __init__(self, points):
            self.points = points
            self.canvas = None

        def update_size(self):
            self.left = min([p.x for p in points])
            self.right = max([p.x for p in points])
            self.top = min([p.y for p in points])
            self.bot = max([p.y for p in points])
            self.size = ((self.right - self.left + 1) *
                         (self.bot - self.top + 1))

        def draw_canvas(self):
            x = self.left
            y = self.top
            w = self.right - x + 1
            h = self.bot - y + 1
            self.canvas = [[Canvas.BLANK_CANVAS for i in range(w)] 
                           for j in range(h)]
            for p in self.points:
                self.canvas[p.y - y][p.x - x] = Canvas.BRUSH_STROKE

        def __str__(self):
            return '\n'.join([''.join(r) for r in self.canvas])

    with open(filename, 'r') as f:
        points = f.readlines()
    points = [re.split('<|, |>|\n', p) for p in points]
    points = [Point(p[1], p[2], p[4], p[5]) for p in points]

    c = Canvas(points)
    previous = sys.maxsize
    c.update_size()
    time = 0
    while c.size < previous:
        previous = c.size
        time += 1
        for p in points:
            p.move(1)
        c.update_size()

    time -= 1
    for p in points:
        p.move(-1)

    c.update_size()
    c.draw_canvas()
    print('[10a]')
    print(c)
    print(f'[10b] would need to wait a total of {time} seconds')
