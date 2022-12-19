#!/usr/bin/env python3

import sys
from typing import List, Set, Dict, Tuple


def read_cubes() -> Set[Tuple[int, int, int]]:
    cubes: Set[Tuple[int, int, int]] = set()
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)
        cubes.add((x, y, z))
    return cubes


def cube_neighbours(cube) -> Set[Tuple[int, int, int]]:
    x, y, z = cube
    return {
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    }


def main():
    cubes = read_cubes()
    exposed_side_count = 0
    for cube in cubes:
        neighbours = cube_neighbours(cube)
        exposed_side_count += len(neighbours - cubes)

    print(exposed_side_count)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
