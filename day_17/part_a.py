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


def main():
    line = sys.stdin.readline().strip()
    directions = DirectionFactory(directions=[LEFT if char == '<' else RIGHT for char in line])
    shapes = ShapeFactory(shapes=[HORIZONTAL_LINE, CROSS, RIGHT_ANGLE, VERTICAL_LINE, SQUARE])
    grid: List[ubyte] = [ubyte(0b1111111)]

    for i in range(2_022):
        shape = shapes.next()
        grid_height = len(grid)
        shape_height = len(shape)
        bottom_of_shape_in_grid = grid_height + 3

        while True:
            direction = directions.next()
            if direction == LEFT and not any((line & ubyte(0b1000000) for line in shape)):
                candidate_shape = [line << 1 for line in shape]
                if shape_has_no_collisions(grid, grid_height, bottom_of_shape_in_grid, shape_height, candidate_shape):
                    shape = candidate_shape

            if direction == RIGHT and not any((line & ubyte(0b0000001) for line in shape)):
                candidate_shape = [line >> 1 for line in shape]
                if shape_has_no_collisions(grid, grid_height, bottom_of_shape_in_grid, shape_height, candidate_shape):
                    shape = candidate_shape

            if shape_has_no_collisions(grid, grid_height, bottom_of_shape_in_grid - 1, shape_height, shape):
                bottom_of_shape_in_grid -= 1
            else:
                for shape_index in range(shape_height):
                    grid_index = bottom_of_shape_in_grid + shape_index
                    if grid_index >= grid_height:
                        grid.append(shape[shape_index])
                    else:
                        grid[grid_index] = grid[grid_index] | shape[shape_index]
                break

        # for line in reversed(grid):
        #     r = binary_repr(line).rjust(7, '0')
        #     r = r.replace('0', '.').replace('1', '#')
        #     r = f"|{r}|"
        #     print(r)
        #
        # print()

    y = len(grid) - 1

    print(y)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
