#!/usr/bin/env python3

from __future__ import annotations
from collections import defaultdict
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def points_between(self, point_to: Point):
        if self.x != point_to.x:
            if self.y != point_to.y:
                raise ValueError(f"Cannot provide points not in a straight line between {self} and {point_to}")
            from_val, to_value = sorted([self.x, point_to.x])
            return [Point(x, self.y) for x in range(from_val, to_value + 1)]
        from_val, to_value = sorted([self.y, point_to.y])
        return [Point(self.x, y) for y in range(from_val, to_value + 1)]


def parse_point(point: str) -> Point:
    x, y = point.split(',')
    return Point(x=int(x), y=int(y))


def read_rock_structures() -> defaultdict(set[int]):
    column_heights = defaultdict(set)
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        points = line.split(' -> ')
        points = [parse_point(point) for point in points]
        for from_point, to_point in list(zip(points[:-1], points[1:])):
            for point in from_point.points_between(to_point):
                column_heights[point.x].add(point.y)

    return column_heights


def add_floor(column_heights: defaultdict(set[int])):
    lowest_points = [max(heights) for heights in column_heights.values()]
    lowest_point = max([height for height in lowest_points])
    floor = lowest_point + 2

    for heights in column_heights.values():
        heights.add(floor)

    def default_with_floor():
        return {floor, }

    column_heights.default_factory = default_with_floor


def main():
    column_heights = read_rock_structures()
    add_floor(column_heights)

    sand_units = 0
    while True:
        x = 500
        y = -10

        while True:
            heights_below = list([height for height in column_heights[x] if height > y])

            y = min(heights_below) - 1
            if y + 1 not in column_heights[x - 1]:
                x = x - 1
                y = y + 1
                continue

            if y + 1 not in column_heights[x + 1]:
                x = x + 1
                y = y + 1
                continue

            if x == 500 and y == 0:
                x = None

            break

        sand_units += 1

        if x is None:
            break

        column_heights[x].add(y)

    print(sand_units)

if __name__ == '__main__':
    main()
