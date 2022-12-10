#!/usr/bin/env python3

import sys
from math import copysign

ROPE_LENGTH = 10


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
    rope = [(0, 0)] * ROPE_LENGTH
    visited = {rope[-1], }

    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        direction, distance = line.split(' ')
        for _ in range(int(distance)):
            rope[0] = move_head(rope[0], direction)
            for index in range(1, ROPE_LENGTH):
                rope[index] = adjust_tail(rope[index - 1], rope[index])
                visited.add(rope[-1])

    print(len(visited))


if __name__ == '__main__':
    main()
