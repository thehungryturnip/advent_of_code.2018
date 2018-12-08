#!/usr/bin/python

# 2018-12-06 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':

    class Node():

        def __init__(self, data=None, prev=None, next_=None):
            self.data = data
            self.prev = prev
            self.next_ = next_

        def __str__(self):
            n = self
            string = str(n.data)
            while n.next_:
                n = n.next_
                string += str(n.data)
            return string

    def create_list(data, exclude=None):
        head = None
        tail = None
        for c in line:
            if not c.lower() == exclude:
                n = Node(c)
                if not head:
                    head = n
                if not tail:
                    tail = n
                tail.next_ = n
                tail.next_.prev = tail
                tail = n
        return head, tail

    def react_polymer(head):
        cursor = head
        while cursor:
            if cursor.next_ and cursor.data.swapcase() == cursor.next_.data:
                if cursor is head:
                    cursor = cursor.next_.next_
                    head = cursor
                else:
                    cursor = cursor.prev
                    cursor.next_ = cursor.next_.next_.next_
                    if cursor.next_:
                        cursor.next_.prev = cursor
            else:
                cursor = cursor.next_
        return head

    filename = sys.argv[1]
    print(f'file: {filename}')

    with open(filename, 'r') as file_:
        line = file_.readline().strip()

    head, tail = create_list(line)
    head = react_polymer(head)
    print(f'[05a] {head} is {len(str(head))} long.')

    types = {}
    cursor = head
    while cursor:
        type_ = cursor.data.lower()
        if type_ not in types:
            types[type_] = 1
        cursor = cursor.next_

    removed = None
    shortest = None
    for t in types:
        head, tail = create_list(line, t)
        head = react_polymer(head)
        if not shortest:
            removed = t
            shortest = head
            continue
        if len(str(head)) < len(str(shortest)):
            shortest = head
    print(f'[05b] shortest is by removing {removed}' +
          f' with a length of {len(str(shortest))}.')
