#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

ROTATION_LOOKUP = {
    'L': -1,
    'R': 1,
}


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Action:
    def perform(self, board: Board):
        raise NotImplementedError


@dataclass()
class Turn(Action):
    rotation: int

    def perform(self, board: Board):
        board.direction = Direction((board.direction.value + self.rotation) % len(Direction))


@dataclass()
class Move(Action):
    count: int

    def perform(self, board: Board):
        for _ in range(self.count):
            if not board.move():
                return


@dataclass
class Board:
    board: List[str]
    x: int = field(default=0)
    y: int = field(default=0)
    face_size: int = field(default=0)
    direction: Direction = field(default=Direction.RIGHT)

    def __post_init__(self):
        first_line = self.board[0]
        self.x = first_line.index('.')
        self.face_size = len(first_line.replace(' ', ''))

    def char_at(self, x, y):
        return self.board[y][x]

    def move(self):
        if self.direction == Direction.LEFT:
            new_x = self.x - 1
            new_y = self.y
            new_direction = self.direction

            if new_x < 0 or self.char_at(new_x, self.y) == ' ':
                if new_y < self.face_size:
                    new_x = self.face_size + self.y
                    new_y = self.face_size
                    new_direction = Direction.DOWN
                elif new_y < self.face_size * 2:
                    new_x = self.face_size * 4 - (self.y - self.face_size + 1)
                    new_y = self.face_size * 3 - 1
                    new_direction = Direction.UP
                else:
                    new_x = self.face_size * 2 - (self.y - self.face_size * 2 + 1)
                    new_y = self.face_size * 2 - 1
                    new_direction = Direction.UP

            if self.char_at(new_x, new_y) == '.':
                self.x = new_x
                self.y = new_y
                self.direction = new_direction
                return True
            return False

        if self.direction == Direction.RIGHT:
            new_x = self.x + 1
            new_y = self.y
            new_direction = self.direction

            if new_x == len(self.board[self.y]) or self.char_at(new_x, self.y) == ' ':
                if new_y < self.face_size:
                    new_x = self.face_size * 4 - 1
                    new_y = self.face_size * 2 + (self.face_size - self.y) - 1
                    new_direction = Direction.LEFT
                elif new_y < self.face_size * 2:
                    new_x = self.face_size * 3 + (self.face_size * 2 - self.y) - 1
                    new_y = self.face_size * 2
                    new_direction = Direction.DOWN
                else:
                    new_x = self.face_size * 2 - (self.y - self.face_size * 2 + 1)
                    new_y = self.face_size * 2 - 1
                    new_direction = Direction.RIGHT

            if self.char_at(new_x, new_y) == '.':
                self.x = new_x
                self.y = new_y
                self.direction = new_direction
                return True
            return False

        if self.direction == Direction.UP:
            new_x = self.x
            new_y = self.y - 1
            new_direction = self.direction

            if new_y < 0 or len(self.board[new_y]) <= self.x or self.char_at(self.x, new_y) == ' ':
                if new_x < self.face_size:
                    new_x = self.face_size * 3 - 1 - self.x
                    new_y = 0
                    new_direction = Direction.DOWN
                elif new_x < self.face_size * 2:
                    new_x = self.face_size * 2
                    new_y = self.x - self.face_size
                    new_direction = Direction.RIGHT
                elif new_x < self.face_size * 3:
                    new_x = self.face_size - (self.x - self.face_size * 2) - 1
                    new_y = self.face_size
                    new_direction = Direction.DOWN
                else:
                    new_x = self.face_size * 3 - 1
                    new_y = self.face_size + (self.face_size * 4 - self.x) - 1
                    new_direction = Direction.RIGHT

            print(self.x, self.y)
            print(new_x, new_y)

            if self.char_at(new_x, new_y) == '.':
                self.x = new_x
                self.y = new_y
                self.direction = new_direction
                return True
            return False

        if self.direction == Direction.DOWN:
            new_x = self.x
            new_y = self.y + 1
            new_direction = self.direction

            if new_y == len(self.board) or len(self.board[new_y]) <= self.x or self.char_at(self.x, new_y) == ' ':
                if new_x < self.face_size:
                    new_x = self.face_size * 3 - 1 - self.x
                    new_y = self.face_size * 3 - 1
                    new_direction = Direction.UP
                elif new_x < self.face_size * 2:
                    new_x = self.face_size * 2
                    new_y = self.face_size * 3 - 1 - (self.face_size * 2 - self.x)
                    new_direction = Direction.RIGHT
                elif new_x < self.face_size * 3:
                    new_x = self.face_size - (self.x - self.face_size * 2) - 1
                    new_y = self.face_size * 2 - 1
                    new_direction = Direction.UP
                else:
                    new_x = 0
                    new_y = self.face_size + (self.face_size * 4 - self.x) - 1
                    new_direction = Direction.RIGHT

            if self.char_at(new_x, new_y) == '.':
                self.x = new_x
                self.y = new_y
                self.direction = new_direction
                return True
            return False

    def display_board(self):
        dir_char = None
        if self.direction == Direction.UP:
            dir_char = '^'
        elif self.direction == Direction.RIGHT:
            dir_char = '>'
        elif self.direction == Direction.DOWN:
            dir_char = 'v'
        elif self.direction == Direction.LEFT:
            dir_char = '<'

        for y in range(len(self.board)):
            if y == self.y:
                print(self.board[y][:self.x] + dir_char + self.board[y][self.x + 1:])
            else:
                print(self.board[y])


def read_board_and_actions() -> Tuple[Board, List[Action]]:
    board = []
    actions_str = None
    face_size = None
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip('\n')
        if not line:
            continue

        print(line)
        chars = set(list(line))
        if chars - {' ', '.', '#', }:
            actions_str = line
            break

        board.append(line)

    print(board)
    print(actions_str)
    print(line)
    actions = []
    number = ''
    for char in actions_str:
        if char in ROTATION_LOOKUP.keys():
            actions.append(Move(count=int(number)))
            actions.append(Turn(rotation=ROTATION_LOOKUP[char]))
            number = ''
        else:
            number += char

    if number:
        actions.append(Move(count=int(number)))

    return Board(board=board), actions


def main():
    board, actions = read_board_and_actions()
    print(board)
    print(actions)
    for action in actions:
        print(board.display_board())
        print()
        action.perform(board=board)

    print(board.display_board())
    print()
    print(1000 * (board.y + 1) + 4 * (board.x + 1) + board.direction.value)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
