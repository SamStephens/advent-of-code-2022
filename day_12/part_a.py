#!/usr/bin/env python3

from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def direction_to(self, point_to: Vector):
        return Vector(x=point_to.x - self.x, y=point_to.y - self.y)

    def point_in_direction(self, direction: Vector):
        return Vector(x=self.x + direction.x, y=self.y + direction.y)


LEFT = Vector(x=-1, y=0)
RIGHT = Vector(x=1, y=0)
UP = Vector(x=0, y=-1)
DOWN = Vector(x=0, y=1)


@dataclass(frozen=True)
class Grid:
    grid: List[List[int]]
    starting_position: Vector
    finishing_position: Vector
    x_length: int = None
    y_length: int = None

    def __post_init__(self):
        object.__setattr__(self, 'x_length', len(self.grid[0]))
        object.__setattr__(self, 'y_length', len(self.grid))

    def in_bounds(self, point: Vector):
        return 0 <= point.x < self.x_length and 0 <= point.y < self.y_length

    def value_at(self, point: Vector):
        return self.grid[point.y][point.x]

    def traversable(self, point: Vector, next_point: Vector):
        change = self.value_at(next_point) - self.value_at(point)
        return change <= 1

    def neighbours(self, point: Vector):
        neighbours = [
            point.point_in_direction(LEFT),
            point.point_in_direction(RIGHT),
            point.point_in_direction(UP),
            point.point_in_direction(DOWN),
        ]
        neighbours = [neighbour for neighbour in neighbours if self.in_bounds(neighbour)]
        neighbours = [neighbour for neighbour in neighbours if self.traversable(point, neighbour)]
        return set(neighbours)


def read_grid() -> Grid:
    grid = []
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        grid.append([char for char in line])

    starting_position = None
    finishing_position = None
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 'S':
                grid[y][x] = 'a'
                starting_position = Vector(x=x, y=y)
            elif grid[y][x] == 'E':
                grid[y][x] = 'z'
                finishing_position = Vector(x=x, y=y)
            grid[y][x] = ord(grid[y][x]) - ord('a')

    return Grid(grid=grid, starting_position=starting_position, finishing_position=finishing_position)


def find_min_distance_path(grid: Grid):
    candidates = {grid.starting_position, }
    visited = set()
    distance = 0
    while True:
        distance += 1
        previous_candidates = candidates
        candidates = set()
        for point in previous_candidates:
            for neighbour in grid.neighbours(point):
                candidates.add(neighbour)
        candidates -= visited
        if not candidates:
            raise Exception('Failed to find path')
        if grid.finishing_position in candidates:
            return distance


def main():
    grid = read_grid()
    min_distance = find_min_distance_path(grid)
    print(min_distance)


if __name__ == '__main__':
    main()
