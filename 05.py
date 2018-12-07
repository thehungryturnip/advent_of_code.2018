#!/usr/bin/python

# 2018-12-06 bob.p.wei@gmail.com

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

    filename = sys.argv[1]
    print(f'file: {filename}')

    head = None
    tail = None
    with open(filename, 'r') as file_:
        c = file_.read(1)
        while c:
            if not c.isspace():
                n = Node(c)
                if not head:
                    head = n
                if not tail:
                    tail = n
                tail.next_ = n
                tail.next_.prev = tail
                tail = n
            c = file_.read(1)
    print(head)
    
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
    print(f'{head} is {len(str(head))} long.')
