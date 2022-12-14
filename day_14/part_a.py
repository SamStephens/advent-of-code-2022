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


def main():
    column_heights = read_rock_structures()

    sand_units = 0
    while True:
        x = 500
        y = 0

        while True:
            heights_below = list([height for height in column_heights[x] if height > y])
            if not heights_below:
                x = None
                break

            y = min(heights_below) - 1
            if y + 1 not in column_heights[x - 1]:
                x = x - 1
                y = y + 1
                continue

            if y + 1 not in column_heights[x + 1]:
                x = x + 1
                y = y + 1
                continue

            break

        if x is None:
            break

        sand_units += 1
        column_heights[x].add(y)

    print(sand_units)

if __name__ == '__main__':
    main()
