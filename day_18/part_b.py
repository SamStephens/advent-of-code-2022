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


def fill_interior_gaps(cubes):
    examined = set()
    internal = set()
    min_x = 999_999_999
    max_x = -999_999_999
    min_y = 999_999_999
    max_y = -999_999_999
    min_z = 999_999_999
    max_z = -999_999_999
    for cube in cubes:
        min_x = min(cube[0], min_x)
        max_x = max(cube[0], max_x)
        min_y = min(cube[1], min_y)
        max_y = max(cube[1], max_y)
        min_z = min(cube[2], min_z)
        max_z = max(cube[2], max_z)
    for cube in cubes:
        neighbours = cube_neighbours(cube)
        neighbours -= cubes
        neighbours -= examined
        for neighbour in neighbours:
            candidates = {neighbour, }
            while True:
                # For each candidate, either we run out of additions, in which case this is interior, or we add a
                # cube that is out of bounds, in which case this is exterior.
                new_candidates = set()
                for candidate in candidates:
                    candidate_neighbours = cube_neighbours(candidate)
                    candidate_neighbours -= cubes
                    candidate_neighbours -= candidates
                    new_candidates |= candidate_neighbours
                if not new_candidates:
                    internal |= candidates
                    examined |= candidates
                    break

                out_of_bounds = False
                for new_candidate in new_candidates:
                    if not (min_x <= new_candidate[0] <= max_x) or not (min_y <= new_candidate[1] <= max_y) or not (min_z <= new_candidate[2] <= max_z):
                        out_of_bounds = True
                        break
                if out_of_bounds:
                    examined |= candidates
                    examined |= new_candidates
                    break

                candidates |= new_candidates
    return cubes | internal


def main():
    cubes = read_cubes()
    cubes = fill_interior_gaps(cubes)
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
