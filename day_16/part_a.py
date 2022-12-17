#!/usr/bin/env python3

from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import List, Set, Dict

TIME_TO_COMPLETE = 30


@dataclass
class Valve:
    name: str
    flow_rate: int
    linked_valves: List[Valve]
    valve_time_to_turn_on: Dict[Valve, int]

    def __hash__(self):
        return id(self)


def read_valves() -> List[Valve]:
    valves: Dict[str, Valve] = {}
    valve_linkages: Dict[str, List[str]] = {}
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        groups = re.fullmatch(
            "Valve ([A-Z]+) has flow rate=(\\d+); tunnels? leads? to valves? ([A-Z, ]+)",
            line,
        ).groups()
        valve_name, flow_rate, linked_valve_names = groups
        flow_rate = int(flow_rate)
        linked_valve_names = linked_valve_names.split(', ')

        valves[valve_name] = Valve(
            name=valve_name,
            flow_rate=flow_rate,
            linked_valves=None,
            valve_time_to_turn_on=None,
        )
        valve_linkages[valve_name] = linked_valve_names

    for valve in valves.values():
        linked_valves = valve_linkages[valve.name]
        linked_valves = [valves[valve_name] for valve_name in linked_valves]
        valve.linked_valves = linked_valves

    valves: List[Valve] = list(valves.values())
    valves.sort(key=lambda v: v.name)
    return valves


def populate_flow_valve_distances(valves: Set[Valve]):
    for valve in [v for v in valves if v.name == 'AA' or v.flow_rate > 0]:
        visited_valves = {valve, }
        starting_valves = {valve, }
        valve_time_to_turn_on = {}
        distance = 0
        while True:
            distance += 1
            next_valves = set()
            for v in starting_valves:
                for n in v.linked_valves:
                    if n not in visited_valves:
                        next_valves.add(n)
                        visited_valves.add(n)
            if not next_valves:
                break
            for n in next_valves:
                if n.flow_rate > 0:
                    valve_time_to_turn_on[n] = distance + 1
            starting_valves = next_valves
        valve.valve_time_to_turn_on = valve_time_to_turn_on


def max_flow_for_given_minute(
        current_valve: Valve,
        candidate_valves: Set[Valve],
        open_valves: Set[Valve],
        minute: int) -> int:
    flow_for_this_minute = sum([valve.flow_rate for valve in open_valves])

    max_flow_from_this_minute_onward = flow_for_this_minute * (TIME_TO_COMPLETE + 1 - minute)

    for next_valve in candidate_valves:
        valve_time_to_turn_on = current_valve.valve_time_to_turn_on[next_valve]
        if minute + valve_time_to_turn_on > TIME_TO_COMPLETE:
            continue

        max_flow_after_valve_open = max_flow_for_given_minute(
            current_valve=next_valve,
            candidate_valves=candidate_valves - {next_valve, },
            open_valves=open_valves | {next_valve, },
            minute=minute + valve_time_to_turn_on
        )
        max_flow_from_this_minute_onward = max(
            max_flow_from_this_minute_onward,
            flow_for_this_minute * valve_time_to_turn_on + max_flow_after_valve_open,
        )

    return max_flow_from_this_minute_onward


def main():
    valves = read_valves()
    populate_flow_valve_distances(set(valves))
    candidate_valves = set(valves[0].valve_time_to_turn_on.keys())
    max_flow_rate = max_flow_for_given_minute(
        current_valve=valves[0],
        candidate_valves=candidate_valves,
        open_valves=set(),
        minute=1,
    )
    print(max_flow_rate)


if __name__ == '__main__':
    import cProfile
    import re

    cProfile.run('main()')
    # main()
