#!/usr/bin/env python

# 2019-09-26 thehungryturnip@gmail.com

import sys
from collections import namedtuple

class Processor:

    __REGISTER_COUNT = 6

    __OPS = {
            '#ip': '_Processor__setp',
            'addr': '_Processor__addr',
            'addi': '_Processor__addi',
            'mulr': '_Processor__mulr',
            'muli': '_Processor__muli',
            'banr': '_Processor__banr',
            'bani': '_Processor__bani',
            'borr': '_Processor__borr',
            'bori': '_Processor__bori',
            'setr': '_Processor__setr',
            'seti': '_Processor__seti',
            'gtir': '_Processor__gtir',
            'gtri': '_Processor__gtri',
            'gtrr': '_Processor__gtrr',
            'eqir': '_Processor__eqir',
            'eqri': '_Processor__eqri',
            'eqrr': '_Processor__eqrr',
        }

    def __init__(self):
        self.__pntr = 0
        self.__prog = []

    def add_instruction(self, ins):
        if ins:
            func = getattr(self, Processor.__OPS.get(ins[0], ''), None)
            if func == self.__setp:
                self.__setp(*ins[1:])
                return
            if func:
                self.__prog.append([func] + [int(a) for a in ins[1:4]])

    def program_str(self):
        prog_str = f'#ip {self.__pntr}'
        for i, v in enumerate(self.__prog):
            prog_str += f'\n{i:2d} {v[0].__name__} {v[1:]}'
        return prog_str

    def run(self, input_=None):
        i = 0
        self.__init(input_)
        while True: # assumes that the program halts
            index = self.__reg[self.__pntr]
            if not (0 <= index < len(self.__prog)) or index == 35:
                return self.__reg
            ins = self.__prog[index]
            ins[0](*ins[1:])
            self.__reg[self.__pntr] += 1

    def __init(self, input_):
        if not input_:
            self.__reg = [0] * Processor.__REGISTER_COUNT
        else:
            self.__reg = list(input_)

    def __incr(self):
        self.__addi(0, 1, 0)

    def __setp(self, i):
        self.__pntr = int(i)

    def __addr(self, r_a, r_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] + self.__reg[r_b] 

    def __addi(self, r_a, v_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] + v_b

    def __mulr(self, r_a, r_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] * self.__reg[r_b]

    def __muli(self, r_a, v_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] * v_b

    def __banr(self, r_a, r_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] & self.__reg[r_b]

    def __bani(self, r_a, v_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] & v_b

    def __borr(self, r_a, r_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] | self.__reg[r_b]

    def __bori(self, r_a, v_b, r_c):
        self.__reg[r_c] = self.__reg[r_a] | v_b

    def __setr(self, r_a, _, r_c):
        self.__reg[r_c] = self.__reg[r_a]

    def __seti(self, v_a, _, r_c):
        self.__reg[r_c] = v_a

    def __gtir(self, v_a, r_b, r_c):
        if v_a > self.__reg[r_b]:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

    def __gtri(self, r_a, v_b, r_c):
        if self.__reg[r_a] > v_b:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

    def __gtrr(self, r_a, r_b, r_c):
        if self.__reg[r_a] > self.__reg[r_b]:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

    def __eqir(self, v_a, r_b, r_c):
        if v_a == self.__reg[r_b]:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

    def __eqri(self, r_a, v_b, r_c):
        if self.__reg[r_a] == v_b:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

    def __eqrr(self, r_a, r_b, r_c):
        if self.__reg[r_a] == self.__reg[r_b]:
            self.__reg[r_c] = 1
        else:
            self.__reg[r_c] = 0

if __name__ == '__main__':

    filename = sys.argv[1]
    print(f'filename: {filename}')

    p = Processor()

    with open(filename, 'r') as f:
        lines = f.read().split('\n')

    for l in lines:
        p.add_instruction(l.split())

    # print('program:')
    # print(p.program_str())

    reg = p.run()
    print(f'[19a] When the program halts, the registers are {reg}, with'
          f' {reg[0]} at register 0.')

    reg = p.run([1, 0, 0, 0, 0, 0])
    print(f'[19b] The registers are {reg} after number generation')
