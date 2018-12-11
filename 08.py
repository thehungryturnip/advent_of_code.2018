#!/usr/bin/python

# 2018-12-10 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    
    class Node:

        def __init__(self, name):
            self.name = name
            self.children = []
            self.data = []

        def __str__(self):
            string = f'{self.name}:{[c.name for c in self.children]}:{self.data}\n'
            for c in self.children:
                string += c.__str__()
            return string

        def __repr__(self):
            return self.__str__()

    def create_node(index, data):
        node = Node(index)
        children_count = data.pop()
        data_count = data.pop()
        for c in range(children_count):
            index += 1
            child, index = create_node(index, data)
            node.children.append(child)
        for d in range(data_count):
            node.data.append(data.pop())
        return node, index

    def sum_meta(node):
        total = 0
        for d in node.data:
            total += d
        for c in node.children:
            total += sum_meta(c)
        return total

    filename = sys.argv[1]
    print(f'file: {filename}')

    with open(filename, 'r') as f:
        data = f.readline().split()

    data = [int(d) for d in data]
    data.reverse()
    head, index = create_node(0, data)
    # print(head)

    meta_total = sum_meta(head)
    print(f'[08a] sum of all meta data is: {meta_total}')
