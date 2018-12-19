#!/usr/bin/python

# 2018-12-19 thehungryturnip@gmail.com

import sys
from heapq import heappush, heappop

if __name__ == '__main__':

    class Cart:

        FACING = {
                'UP': 0,
                'RIGHT': 1,
                'DOWN': 2,
                'LEFT': 3,
                }

        # use in conjuction with "FACING"
        MOVEMENT = {
                0: (-1, 0),
                1: (0, 1),
                2: (1, 0),
                3: (0, -1),
                }

        TURN = {
                'LEFT': -1,
                'STRAIGHT': 0,
                'RIGHT': 1,
                }

        def __init__(self, facing):
            self.facing = facing
            self.next_turn = Cart.TURN['LEFT']

        @property
        def facing(self):
            return self.__facing

        @facing.setter
        def facing(self, facing):
            while facing < Cart.FACING['UP']:
                facing += len(Cart.FACING)
            while facing > Cart.FACING['LEFT']:
                facing -= len(Cart.FACING)
            self.__facing = facing

        @property
        def next_turn(self):
            return self.__next_turn

        @next_turn.setter
        def next_turn(self, turn):
            while turn < Cart.TURN['LEFT']:
                turn += len(Cart.TURN)
            while turn > Cart.TURN['RIGHT']:
                turn -= len(Cart.TURN)
            self.__next_turn = turn

        def intersection_turn(self):
            self.facing += self.next_turn
            self.next_turn += 1

        def move(self):
            return Cart.MOVEMENT[self.facing][0], Cart.MOVEMENT[self.facing][1]

        def __str__(self):
            return f'{self.facing}:{self.next_turn}'

        def __repr__(self):
            return self.__str__()

    class Map:

        CART_DIRECTION = {
                '^': Cart.FACING['UP'],
                '>': Cart.FACING['RIGHT'],
                'v': Cart.FACING['DOWN'],
                '<': Cart.FACING['LEFT'],
                }

        # reverse search of CART_DIRECTION
        CART_SYMBOL = {
                Cart.FACING['UP']: '^',
                Cart.FACING['RIGHT']: '>',
                Cart.FACING['DOWN']: 'v',
                Cart.FACING['LEFT']: '<',
                }

        TURN_CASE = {
                (Cart.FACING['UP'], '\\'): -1,
                (Cart.FACING['RIGHT'], '\\'): 1,
                (Cart.FACING['DOWN'], '\\'): -1,
                (Cart.FACING['LEFT'], '\\'): 1,
                (Cart.FACING['UP'], '/'): 1,
                (Cart.FACING['RIGHT'], '/'): -1,
                (Cart.FACING['DOWN'], '/'): 1,
                (Cart.FACING['LEFT'], '/'): -1,
                }

        def __init__(self, rows, cols):
            self.map = [[' ' for c in range(cols)] for r in range(rows)]
            self.carts_map = [[None for c in range(cols)] for r in range(rows)]
            self.cart_locs = []

        def set_track(self, r, c, track):
            if track in '^>v<':
                cart = Cart(Map.CART_DIRECTION[track])
                self.carts_map[r][c] = cart
                heappush(self.cart_locs, (r, c))
                if track in '^v':
                    track = '|'
                if track in '<>':
                    track = '-'
            self.map[r][c] = track

        def move_cart(self, r, c):
            cart = self.carts_map[r][c]
            self.carts_map[r][c] = None
            dr, dc = cart.move()
            r += dr
            c += dc
            if self.carts_map[r][c]:
                return (r, c)
            self.carts_map[r][c] = cart
            heappush(self.cart_locs, (r, c))
            track = self.map[r][c]
            if track == '+':
                cart.intersection_turn()
            else:
                cart.facing += Map.TURN_CASE.get((cart.facing, track), 0)

        def proceed(self):
            old_locs = self.cart_locs
            self.cart_locs = []
            while old_locs:
                loc = heappop(old_locs)
                crashed = self.move_cart(loc[0], loc[1])
                if crashed:
                    return crashed

        def __str__(self):
            string = ''
            for r in range(len(self.map)):
                for c in range(len(self.map[r])):
                    if self.carts_map[r][c]:
                        string += Map.CART_SYMBOL[self.carts_map[r][c].facing]
                    else:
                        string += self.map[r][c]
                string += '\n'
            return string[:-1] # exclude the last '\n'

        def __repr__(self):
            return self.__str__()

    def find_max_cols(rows):
        cols = 0
        for r in range(len(rows)):
            rows[r] = rows[r][:-1]
            if len(rows[r]) > cols:
                cols = len(rows[r])
        return cols

    def populate_map(rows, m):
        for r in range(len(rows)):
            for c in range(len(rows[r])):
                m.set_track(r, c, rows[r][c])

    filename = sys.argv[1]
    print(f'file: {filename}')

    with open(filename, 'r') as f:
        rows = f.readlines()

    m = Map(len(rows), find_max_cols(rows))
    populate_map(rows, m)

    crashed = None
    while not crashed:
        crashed = m.proceed()

    print(f'[13a] first crash occured at coordinate' +
          f' ({crashed[1]},{crashed[0]})')
