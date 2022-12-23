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
    direction: Direction = field(default=Direction.RIGHT)

    def __post_init__(self):
        self.x = self.board[0].index('.')

    def char_at(self, x, y):
        return self.board[y][x]

    def move(self):
        if self.direction == Direction.LEFT:
            new_x = self.x - 1
            while new_x < 0 or self.char_at(new_x, self.y) == ' ':
                if new_x < 0:
                    new_x = len(self.board[self.y])
                new_x -= 1
            if self.char_at(new_x, self.y) == '.':
                self.x = new_x
                return True
            return False

        if self.direction == Direction.RIGHT:
            new_x = self.x + 1
            while new_x == len(self.board[self.y]) or self.char_at(new_x, self.y) == ' ':
                if new_x == len(self.board[self.y]):
                    new_x = -1
                new_x += 1
            if self.char_at(new_x, self.y) == '.':
                self.x = new_x
                return True
            return False

        if self.direction == Direction.UP:
            new_y = self.y - 1
            while new_y < 0 or len(self.board[new_y]) <= self.x or self.char_at(self.x, new_y) == ' ':
                if new_y < 0:
                    new_y = len(self.board)
                new_y -= 1
            if self.char_at(self.x, new_y) == '.':
                self.y = new_y
                return True
            return False

        if self.direction == Direction.DOWN:
            new_y = self.y + 1
            while new_y == len(self.board) or len(self.board[new_y]) <= self.x or self.char_at(self.x, new_y) == ' ':
                if new_y == len(self.board):
                    new_y = -1
                new_y += 1
            if self.char_at(self.x, new_y) == '.':
                self.y = new_y
                return True
            return False


def read_board_and_actions() -> Tuple[Board, List[Action]]:
    board = []
    actions_str = None
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
        print(board.x + 1, board.y + 1, board.direction)
        action.perform(board=board)
        print(action)
        print(board.x + 1, board.y + 1, board.direction)
        print()

    print(1000 * (board.y + 1) + 4 * (board.x + 1) + board.direction.value)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
