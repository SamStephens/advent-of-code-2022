#!/usr/bin/env python3
import itertools
import sys
import re
from dataclasses import dataclass
from typing import List, Set
from collections import defaultdict


@dataclass(frozen=True)
class Sensor:
    x: int
    y: int
    beacon_distance: int

    def range_for_y(self, target_y) -> range:
        y_distance = abs(self.y - target_y)
        x_distance = self.beacon_distance - y_distance
        if x_distance < 0:
            return None

        return range(self.x - x_distance, self.x + x_distance + 1)


def read_sensors() -> List[Sensor]:
    sensors = []
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        groups = re.fullmatch(
            "Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)",
            line,
        ).groups()
        sensor_x, sensor_y, beacon_x, beacon_y = groups
        sensor_x, sensor_y, beacon_x, beacon_y = int(sensor_x), int(sensor_y), int(beacon_x), int(beacon_y)
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        sensors.append(Sensor(sensor_x, sensor_y, distance))

    return sensors


def combine_ranges(ranges: Set[range]):
    while True:
        removed_ranges = None
        combined_range = None
        for range_a, range_b in itertools.permutations(ranges, 2):
            if range_a.stop > range_b.start and range_a.start < range_b.stop:
                removed_ranges = range_a, range_b
                combined_range = range(
                    min(range_a.start, range_b.start),
                    max(range_a.stop, range_b.stop),
                )
                break

        if not removed_ranges:
            break

        for r in removed_ranges:
            ranges.remove(r)

        ranges.add(combined_range)

    return ranges


def main():
    max_coord = sys.argv[1]
    max_coord = int(max_coord)
    sensors = read_sensors()

    for y in range(0, max_coord + 1):
        ranges = (sensor.range_for_y(y) for sensor in sensors)
        ranges = set([r for r in ranges if r is not None])
        combine_ranges(ranges)

        range_for_gap = [r for r in ranges if 0 < r.start <= max_coord + 1]
        if any(range_for_gap):
            print((range_for_gap[0].start - 1) * 4000000 + y)
            break


if __name__ == '__main__':
    main()
