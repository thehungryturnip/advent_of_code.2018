#!/usr/bin/python

# 2019-06-10 thuhungryturnip@gmail.com

import re
import sys
from heapq import heappush, heappop, heapify
from enum import Enum, auto

if __name__ == '__main__':

    INPUT_PREFIX = 'Before:'
    OUTPUT_PREFIX = 'After:'
    DELIMITERS = '[\[,\]]'

    class Processor():

        class Ops(Enum):
            _addr = auto()
            _addi = auto()
            _mulr = auto()
            _muli = auto()
            _banr = auto()
            _bani = auto()
            _borr = auto()
            _bori = auto()
            _setr = auto()
            _seti = auto()
            _gtir = auto()
            _gtri = auto()
            _gtrr = auto()
            _eqir = auto()
            _eqri = auto()
            _eqrr = auto()

            def __lt__(self, other):
                return self.value < other.value

        def __init__(self):
            self.reset_registers()
            self.map = [[None for op_codes in Processor.Ops]
                        for op_ids in Processor.Ops]

        def reset_registers(self):
            self.reg = [0, 0, 0, 0]

        def sample(self, sample):
            successes = 0
            for op in Processor.Ops:
                self.reg = sample.input[:]
                code = sample.operation[0]
                args = sample.operation[1:]
                getattr(self, op.name)(*args)
                if self.reg == sample.output:
                    self.map[op.value - 1][code] = True
                    successes += 1
                else:
                    self.map[op.value - 1][code] = False
            return successes

        def analyze(self):
            in_progress = []

            for op in Processor.Ops:
                mapping = self.map[op.value - 1]
                heappush(in_progress, (sum(m for m in mapping), op))

            while in_progress:
                entry = heappop(in_progress)
                if entry[0] == 1:
                    op_code = self.map[entry[1].value - 1].index(True)
                    old_progress = in_progress
                    in_progress = []
                    while old_progress:
                        other = heappop(old_progress)
                        mapping = self.map[other[1].value - 1]
                        if mapping[op_code]:
                            mapping[op_code] = False
                        heappush(in_progress, (sum(m for m in mapping), other[1]))

            self.code_to_op = {}
            for op in Processor.Ops:
                code = self.map[op.value - 1].index(True)
                self.code_to_op[code] = op

        def execute(self, instructions):
            for i in instructions:
                code = i[0]
                args = i[1:]
                getattr(self, self.code_to_op[code].name)(*args)

        def map_str(self):
            map_str = ''
            for op in Processor.Ops:
                if map_str:
                    map_str += '\n'
                map_str += op.name + ' '
                map_ = self.map[op.value - 1][:]
                map_ = map(lambda v: 'X' if v else '.', map_)
                map_str += ''.join(list(map_))
            return map_str

        def _claim_mapping(self, op):
            op_map = self.map[op.value - 1]
            for c in len(op_map):
                if c:
                    for other_op in Processor.Ops:
                        if self.map[other_op.value - 1][c]:
                            self.map[other_op.vallue - 1][c] = False

        def _addr(self, r_a, r_b, r_c):
            self.reg[r_c] = self.reg[r_a] + self.reg[r_b] 

        def _addi(self, r_a, v_b, r_c):
            self.reg[r_c] = self.reg[r_a] + v_b

        def _mulr(self, r_a, r_b, r_c):
            self.reg[r_c] = self.reg[r_a] * self.reg[r_b]

        def _muli(self, r_a, v_b, r_c):
            self.reg[r_c] = self.reg[r_a] * v_b

        def _banr(self, r_a, r_b, r_c):
            self.reg[r_c] = self.reg[r_a] & self.reg[r_b]

        def _bani(self, r_a, v_b, r_c):
            self.reg[r_c] = self.reg[r_a] & v_b

        def _borr(self, r_a, r_b, r_c):
            self.reg[r_c] = self.reg[r_a] | self.reg[r_b]

        def _bori(self, r_a, v_b, r_c):
            self.reg[r_c] = self.reg[r_a] | v_b

        def _setr(self, r_a, _, r_c):
            self.reg[r_c] = self.reg[r_a]

        def _seti(self, v_a, _, r_c):
            self.reg[r_c] = v_a

        def _gtir(self, v_a, r_b, r_c):
            if v_a > self.reg[r_b]:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

        def _gtri(self, r_a, v_b, r_c):
            if self.reg[r_a] > v_b:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

        def _gtrr(self, r_a, r_b, r_c):
            if self.reg[r_a] > self.reg[r_b]:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

        def _eqir(self, v_a, r_b, r_c):
            if v_a == self.reg[r_b]:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

        def _eqri(self, r_a, v_b, r_c):
            if self.reg[r_a] == v_b:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

        def _eqrr(self, r_a, r_b, r_c):
            if self.reg[r_a] == self.reg[r_b]:
                self.reg[r_c] = 1
            else:
                self.reg[r_c] = 0

    class Sample:
        def __str__(self):
            return f'{self.input} {self.operation} {self.output}'

        def __repr__(self):
            return self.__str__()

    filename = sys.argv[1]
    print(f'filename: {filename}')

    samples = []
    sample = None
    instructions = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            if line.startswith(INPUT_PREFIX):
                sample = Sample()
                split = re.split(DELIMITERS, line)
                sample.input = [int(i) for i in split[1:5]]
            elif line.startswith(OUTPUT_PREFIX):
                split = re.split(DELIMITERS, line)
                sample.output = [int(o) for o in split[1:5]]
                samples.append(sample)
                sample = None
            elif sample is not None:
                sample.operation = [int(o) for o in line.split()[:4]]
            elif line is not '\n':
                instructions.append([int(i) for i in line.split()[:4]])
            line = f.readline()

    p = Processor()
    matching_samples = []
    for t in samples:
        if p.sample(t) >=3:
            matching_samples.append(t)
    # matching_samples = [t in samples if p.tune(t) >= 3]
    print(f'[16a] {len(matching_samples)} samples matched 3 or more operations.')

    p.analyze()
    print(p.map_str())

    p.reset_registers()
    p.execute(instructions)
    print(p.reg)
    print(f'[16b] The value of register 0 is {p.reg[0]} after executing the instructions.')
