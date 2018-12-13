#!/usr/bin/python

# 2018-12-12 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    serial_number = int(sys.argv[1])
    print(f'serial number: {serial_number}')
    grid_size = int(sys.argv[2])
    print(f'grid size: {grid_size}')

    class FuelCell:

        def __init__(self, x, y, serial_number):
            self.x = x
            self.y = y
            self.serial_number = serial_number
            rack_id = x + 10
            power = rack_id * y
            power += serial_number
            power *= rack_id
            power = power % 1000 // 100 # getting the 100th digit
            power -= 5
            self.power = power

        def __str__(self):
            return f'({self.x},{self.y},{self.serial_number}):{self.power}'
        
        def __repr__(self):
            return self.__str__()

    class FuelGrid:

        def __init__(self, size, serial_number):
            self.size = size
            self.serial_number = serial_number
            self.cells = [[FuelCell(x + 1, y + 1, serial_number) 
                           for x in range(size)]
                          for y in range(size)]
            self.create_summed_table()

        def create_summed_table(self):
            self.summed = []
            for y in range(self.size):
                self.summed.append([])
                for x in range(self.size):
                    s = self.cells[y][x].power
                    if not x == 0:
                        s += self.summed[y][x - 1]
                    if not y == 0:
                        s += self.summed[y - 1][x]
                    if not x == 0 and not y == 0:
                        s -= self.summed[y - 1][x - 1]
                    self.summed[y].append(s)

        def get_power_at(self, x, y, size=3):
            # 1 to account for 1-based indexing. 1 to account for shifting the
            # square
            x -= 2
            y -= 2
            power = self.summed[y + size][x + size]
            if x > 0:
                power -= self.summed[y + size][x]
            if y > 0:
                power -= self.summed[y][x + size]
            if x > 0 and y > 0:
                power += self.summed[y][x]
            return power

        def get_max_power(self, size=3):
            best_power = -sys.maxsize
            for x in range(self.size - size + 1):
                for y in range(self.size - size + 1):
                    power = self.get_power_at(x + 1, y + 1, size)
                    if power > best_power:
                        best_x = x
                        best_y = y
                        best_power = power
            return best_x + 1, best_y + 1, best_power

    def test_cells():
        data = ((122, 79, 57),
                (217, 196, 39),
                (101, 153, 71))
        for d in data:
            c = FuelCell(*d)
            print(c)

    # test_cells()
    grid = FuelGrid(grid_size, serial_number)
    
    best_x, best_y, best_p = grid.get_max_power()
    print(f'[11a] best power for serial number {serial_number} is at'
          f' ({best_x},{best_y}) at {best_p}')

    best_p = -sys.maxsize
    for s in range(1, grid_size + 1):
        x, y, p = grid.get_max_power(s)
        if p > best_p:
            best_x = x
            best_y = y
            best_s = s
            best_p = p
    print(f'[11b] best power for serial number {serial_number} is at'
          f' ({best_x},{best_y},{best_s}) {best_p}')

