#!/usr/bin/python

# 2018-12-19 thehungryturnip@gmail.com

import sys
from collections import deque, namedtuple 
from enum import Enum, auto
from heapq import heappush, heappop

if __name__ == '__main__':

    class Coord(namedtuple('Coord', ['r', 'c'])):

        def adjacent(self):
            return [self + delta for delta
                    in [Coord(-1,0), Coord(0,-1), Coord(0,1), Coord(1,0)]]

        def distance_to(self, other):
            return abs(self.r - other.r) + abs(self.c - other.c)

        def __add__(self, other):
            return Coord(self.r + other.r, self.c + other.c)

        def __sub__(self, other):
            return Coord(self.r - other.r, self.c - other.c)

        def __str__(self):
            return f'({self.r},{self.c})'

        def __repr__(self):
            return self.__str__()

    class Piece:

        class Type(Enum):
            WALL = auto()
            ELF = auto()
            GOBLIN = auto()
        
        def __init__(self, piece_type):
            self.type = piece_type
            if (self.type != Piece.Type.WALL):
                # self.hp = 2
                self.hp = 200
                self.power = 3

        def is_alive(self):
            if self.type == Piece.Type.WALL:
                return False
            return self.hp > 0

        def attack(self, other):
            other.hp -= self.power

        def __str__(self):
            return f'{{{self.type},{getattr(self,"hp",None)}}}'

        def __repr__(self):
            return self.__str__()

    class Field(dict):

        SYMBOL_TO_TYPE = {
                '#': Piece.Type.WALL,
                'E': Piece.Type.ELF,
                'G': Piece.Type.GOBLIN,
                '.': None,
                }

        TYPE_TO_SYMBOL = {
                Piece.Type.WALL: '#',
                Piece.Type.ELF: 'E',
                Piece.Type.GOBLIN: 'G',
                None: '.',
                }

        Path = namedtuple('Path', ['cost', 'coords'])

        def __init__(self, rows, elf_power):
            self.teams = {}
            self.row_count = len(rows)
            self.col_count = 0
            self.elf_died = False
            for r, row in enumerate(rows):
                if (len(row) > self.col_count):
                    self.col_count = len(row)
                for c, symbol in enumerate(row):
                    piece_type = Field.SYMBOL_TO_TYPE[symbol]
                    # Not creating pieces for empty space (i.e. '.').
                    if piece_type:
                        unit = Piece(piece_type)
                        if piece_type == Piece.Type.ELF:
                            unit.power = elf_power
                        self[Coord(r,c)] = unit
                        if piece_type != Piece.Type.WALL:
                            self.teams.setdefault(piece_type, {})
                            self.teams[piece_type][Coord(r, c)] = None

        def process_round(self):
            queue = self._get_unit_coords()
            # print(queue)
            while queue:
                unit_c = heappop(queue)

                # Unit may die before its turn.
                if unit_c not in self:
                    continue

                # print(f'processing:{unit_c}:{self[unit_c]}')
                targets_c = self._get_unit_coords(excludes=self[unit_c].type)

                # Round ends without completing if no more targets.
                if not targets_c:
                    return False, self.elf_died

                unit_c = self._try_move(unit_c, targets_c)
                self._try_attack(unit_c)
            return True, self.elf_died

        def get_total_hp(self):
            return sum([self[m].hp for _, t in self.teams.items() for m in t])

        def _get_unit_coords(self, excludes=None):
            units_c = []
            for team in self.teams:
                if team != excludes:
                    for coord in self.teams[team]:
                        heappush(units_c, coord)
            return units_c

        def _try_move(self, unit_c, targets_c):
            # No need to move if already next to a target.
            for c in unit_c.adjacent():
                for t in targets_c:
                    if c == t:
                        # print(f'target at {t}')
                        return unit_c

            move_targets = set(c 
                               for t in targets_c 
                               for c in t.adjacent() 
                               if c not in self)

            # best_path = None
            # for c in move_targets:
            #     p = self._path_between(unit_c, c)
            #     if not p:
            #         continue
            #     if not best_path:
            #         best_path = p
            #         continue
            #     if p < best_path:
            #         best_path = p

            best_path = self._closest_target(unit_c, move_targets)
            
            if not best_path:
                return unit_c

            # print(f'best_path:{best_path}')
            unit = self[unit_c]
            # new_coord = best_path.coords[1]
            new_coord = best_path[1]
            self[new_coord] = unit
            del self[unit_c]
            self.teams[unit.type][new_coord] = None
            del self.teams[unit.type][unit_c]
            return new_coord

        def _closest_target(self, c_1, move_targets):
            in_progress = deque()
            in_progress.append([c_1])
            visited = set(c_1)
            while in_progress:
                p = in_progress.popleft()
                for c in p[-1].adjacent():
                    if c in visited or c in self:
                        continue
                    if c in move_targets:
                        return p + [c]
                    visited.add(c)
                    in_progress.append(p + [c])
            return None

        def _path_between(self, c_1, c_2):
            # in_progress = [Field.Path(c_1.distance_to(c_2),[c_1])]
            in_progress = [Field.Path(0,[c_1])]
            visited = set(c_1)

            while in_progress:
                p = heappop(in_progress)

                if p.coords[-1] == c_2:
                    return p

                for c in p.coords[-1].adjacent():

                    if c in visited or c in self:
                        continue

                    visited.add(c)
                    # new_path = Field.Path(len(p.coords) + c.distance_to(c_2), 
                    #                       p.coords + [c])
                    new_path = Field.Path(len(p.coords), p.coords + [c])
                    heappush(in_progress, new_path)

            return None

        def _try_attack(self, unit_c):
            unit = self[unit_c]

            # Find all targets.
            targets_c = []
            for c in unit_c.adjacent():
                if (c in self
                        and self[c].is_alive()
                        and self[c].type != unit.type):
                    targets_c.append(c)
            if not targets_c:
                return
            
            # Find target with least hp or reading order (if same hp).
            target_c = min(targets_c, key=lambda c: (self[c].hp, c))
            target = self[target_c]

            # Attack and remove from field if dead
            unit.attack(target)
            if not target.is_alive():
                del self[target_c]
                del self.teams[target.type][target_c]
                if target.type == Piece.Type.ELF:
                    self.elf_died = True
        
        def _str_row(self, r):
            row = ""
            hps = []
            for c in range(self.col_count):
                piece = self.get(Coord(r, c), None)
                if piece:
                    row += Field.TYPE_TO_SYMBOL[piece.type]
                else:
                    row += Field.TYPE_TO_SYMBOL[None]
                if (piece and piece.type != Piece.Type.WALL):
                    hps.append(piece.hp)
            return row + ' ' + ' '.join(str(hp) for hp in hps)

        def __str__(self):
            return '\n'.join([self._str_row(r) for r in range(self.row_count)])

    class Battle:

        def __init__(self, rows, elf_power=3):
            self.field = Field(rows, elf_power)
            self.rounds = 0

        def process_round(self):
            round_complete, _ = self.field.process_round()
            # if self.rounds >= 25:
            #     round_complete = False
            if round_complete:
                self.rounds += 1
            return round_complete

        def elf_dies(self):
            round_complete = True
            while round_complete:
                round_complete, elf_died = self.field.process_round()
                if round_complete:
                    self.rounds += 1
                if elf_died:
                    return True
            return False 

        def hp(self):
            return self.field.get_total_hp()

        def __str__(self):
            return str(self.field)
            
    filename = sys.argv[1]
    print(f'file: {filename}')

    data = []
    with open(filename, 'r') as f:
        line = f.readline().strip()
        while line:
            data.append(line)
            line = f.readline().strip()

    battle = Battle(data)
    print(f'[start!]')
    print(battle)

    while battle.process_round():
        print(f'[{battle.rounds}]')
        print(battle)
    print(f'[finished!]')
    print(battle)

    rounds = battle.rounds
    hp = battle.hp()
    print(f'[15a] Final score: {rounds} x {hp} = {rounds * hp}')

    power = 4
    battle = Battle(data, power)
    print(f'Trying power:{power}')
    while battle.elf_dies():
        print(f'[elf died: {battle.rounds} rounds {battle.hp()} hp]')
        print(battle)
        power += 1
        battle = Battle(data, power)
        print(f'Trying power:{power}')
    print(f'[victory!]')
    print(battle)

    rounds = battle.rounds
    hp = battle.hp()
    print(f'[15b] Final score with power {power}: {rounds} x {hp} = {rounds * hp}')
