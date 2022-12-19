#!/usr/bin/env python3

from __future__ import annotations
import sys
from collections import defaultdict
from dataclasses import field, dataclass
from typing import List, Set
from numpy import ubyte, binary_repr

LEFT = 0
RIGHT = 1

# Multiple line shapes are defined from bottom to top
HORIZONTAL_LINE = [
    ubyte(0b0011110),
]
CROSS = [
    ubyte(0b0001000),
    ubyte(0b0011100),
    ubyte(0b0001000),
]
RIGHT_ANGLE = [
    ubyte(0b0011100),
    ubyte(0b0000100),
    ubyte(0b0000100),
]
VERTICAL_LINE = [
    ubyte(0b0010000),
    ubyte(0b0010000),
    ubyte(0b0010000),
    ubyte(0b0010000),
]
SQUARE = [
    ubyte(0b0011000),
    ubyte(0b0011000),
]


@dataclass
class ShapeFactory:
    shapes: List[List[ubyte]]
    length: int = field(init=False)
    position: int = field(init=False, default=0)

    def __post_init__(self):
        self.__setattr__('length', len(self.shapes))

    def next(self) -> List[ubyte]:
        shape = self.shapes[self.position]
        self.position = (self.position + 1) % self.length
        return shape


@dataclass
class DirectionFactory:
    directions: List[int]
    length: int = field(init=False)
    position: int = field(init=False, default=0)

    def __post_init__(self):
        self.__setattr__('length', len(self.directions))

    def next(self) -> int:
        direction = self.directions[self.position]
        self.position = (self.position + 1) % self.length
        return direction


def shape_has_no_collisions(grid, grid_height, bottom_of_shape_in_grid, shape_height, candidate_shape):
    for shape_index in range(shape_height):
        grid_index = bottom_of_shape_in_grid + shape_index
        if grid_index >= grid_height:
            return True
        if grid[grid_index] & candidate_shape[shape_index]:
            return False
    return True


def attempt_grid_condense(grid):
    previous_row = grid[-1]
    for i in reversed(range(len(grid) - 1)):
        row = grid[i]
        if previous_row | row == ubyte(0b1111111):
            return grid[i:]
        previous_row = row
    return grid


def main():
    line = sys.stdin.readline().strip()
    directions = DirectionFactory(directions=[LEFT if char == '<' else RIGHT for char in line])
    shapes = ShapeFactory(shapes=[HORIZONTAL_LINE, CROSS, RIGHT_ANGLE, VERTICAL_LINE, SQUARE])
    previous_added_rows = defaultdict(list)
    previously_added_repeat = defaultdict(list)
    previously_added_height = defaultdict(list)
    top_of_grid = 0
    grid: List[ubyte] = [ubyte(0b1111111)]
    RANGE = 1_000_000_000_000
    i = 0

    while i < RANGE:
        if shapes.position == 0 and previous_added_rows is not None:
            if not previous_added_rows[directions.position]:
                previous_added_rows[directions.position].append(grid.copy())
                previously_added_repeat[directions.position].append(i)
                previously_added_height[directions.position].append(top_of_grid)
            else:
                try:
                    previous_n = previous_added_rows[directions.position].index(grid)
                    # We've seen a repeat, we can compute based on that repetition
                    previous_i = previously_added_repeat[directions.position][previous_n]
                    previous_height = previously_added_height[directions.position][previous_n]
                    i_between_repeats = i - previous_i
                    number_of_whole_cycles = (RANGE - i) // i_between_repeats
                    i += number_of_whole_cycles * i_between_repeats
                    top_of_grid += number_of_whole_cycles * (top_of_grid - previous_height)
                    previous_added_rows = None
                except ValueError:
                    previous_added_rows[directions.position].append(grid.copy())
                    previously_added_repeat[directions.position].append(i)
                    previously_added_height[directions.position].append(top_of_grid)

        shape = shapes.next()
        grid_length = len(grid)
        shape_length = len(shape)
        bottom_of_shape_in_grid = grid_length + 3

        while True:
            direction = directions.next()
            if direction == LEFT and not any((line & ubyte(0b1000000) for line in shape)):
                candidate_shape = [line << 1 for line in shape]
                if shape_has_no_collisions(grid, grid_length, bottom_of_shape_in_grid, shape_length, candidate_shape):
                    shape = candidate_shape

            if direction == RIGHT and not any((line & ubyte(0b0000001) for line in shape)):
                candidate_shape = [line >> 1 for line in shape]
                if shape_has_no_collisions(grid, grid_length, bottom_of_shape_in_grid, shape_length, candidate_shape):
                    shape = candidate_shape

            if shape_has_no_collisions(grid, grid_length, bottom_of_shape_in_grid - 1, shape_length, shape):
                bottom_of_shape_in_grid -= 1
            else:
                for shape_index in range(shape_length):
                    grid_index = bottom_of_shape_in_grid + shape_index
                    if grid_index >= grid_length:
                        grid.append(shape[shape_index])
                        top_of_grid += 1
                    else:
                        grid[grid_index] = grid[grid_index] | shape[shape_index]
                grid = attempt_grid_condense(grid)
                break

        i += 1

    print(top_of_grid)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
