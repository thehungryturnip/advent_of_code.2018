#!/usr/bin/python

# 2018-12-10 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')

    class Marble:

        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def link_with(self, other):
            self.right = other
            other.left = self

        def remove_left(self):
            n = self.left
            n.left.link_with(self)
            return n

        def __str__(self):
            return str(self.val)

        def __repr__(self):
            return self.__str__()

    class MarbleGame:

        SCORING_MARBLE = 23

        def __init__(self):
            self.zero = Marble(0)
            self.current = self.zero
            self.current.link_with(self.current)
            self.to_play = 1

        def add_marble(self):
            if self.to_play % MarbleGame.SCORING_MARBLE == 0:
                for i in range(6):
                    self.current = self.current.left
                removed = self.current.remove_left()
                score = removed.val + self.to_play
                self.to_play += 1
                return score
            m = Marble(self.to_play)
            self.to_play += 1
            m.link_with(self.current.right.right)
            self.current.right.link_with(m)
            self.current = m
            return 0

        def __str__(self):
            marbles = [self.zero]
            m = self.zero.right
            while m is not self.zero:
                marbles.append(m)
                m = m.right
            return str(marbles)

        def __repr__(self):
            return self.__str__()


    with open(filename, 'r') as f:
        rounds = f.readlines()
    rounds = [r.split() for r in rounds]
    rounds = [(int(r[0]), int(r[6])) for r in rounds]
    # print(rounds)

    for r in rounds:
        g = MarbleGame()
        scores = [0] * r[0]
        p = 0
        for i in range(r[1]):
            score = g.add_marble()
            scores[p] += score
            p += 1
            if p == len(scores):
                p = 0
        highest = max(scores)
        print(f'Game {r} has high score {highest}')
