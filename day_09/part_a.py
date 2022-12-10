#!/usr/bin/env python3

import sys
from math import copysign


def sign(num):
    return int(copysign(1, num))


def move_head(head, direction):
    x, y = head
    if direction == 'L':
        x -= 1
    elif direction == 'R':
        x += 1
    if direction == 'D':
        y -= 1
    elif direction == 'U':
        y += 1
    return x, y


def adjust_tail(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail
    if abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) <= 1:
        return tail_x, tail_y

    if abs(head_y - tail_y) == 0:
        return tail_x + sign(head_x - tail_x), tail_y

    if abs(head_x - tail_x) == 0:
        return tail_x, tail_y + sign(head_y - tail_y)

    return tail_x + sign(head_x - tail_x), tail_y + sign(head_y - tail_y)


def main():
    head = (0, 0)
    tail = (0, 0)
    visited = {tail, }

    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        direction, distance = line.split(' ')
        for _ in range(int(distance)):
            head = move_head(head, direction)
            tail = adjust_tail(head, tail)
            visited.add(tail)

    print(len(visited))


if __name__ == '__main__':
    main()
