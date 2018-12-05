#!/usr/bin/python

# 2018-12-03 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    print(f'file: {filename}')
    sum_ = 0
    with open(filename, 'r') as file_:
        line = file_.readline()
        while line:
            sum_ += int(line)
            line = file_.readline()

    print(f'total: {sum_}')
