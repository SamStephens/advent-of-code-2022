#!/usr/bin/env python3

from __future__ import annotations
import concurrent.futures
import itertools
import sys
from dataclasses import dataclass
from typing import List, Set, Dict
import re

CONCURRENCY = 12
TIME_TO_COMPLETE = 26


@dataclass
class Valve:
    name: str
    flow_rate: int
    linked_valves: List[Valve]
    valve_time_to_turn_on: Dict[Valve, int]

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Valve(name={self.name})"


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


def populate_valve_time_to_turn_on(valves: Set[Valve]):
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
        human_valve: Valve,
        elephant_valve: Valve,
        remaining_human_minute: int,
        remaining_elephant_minute: int,
        candidate_valves: Set[Valve],
        open_valves: Set[Valve],
        minute: int) -> int:

    valves_to_open = set()

    if remaining_human_minute == 0:
        valves_to_open.add(human_valve)
    if remaining_elephant_minute == 0:
        valves_to_open.add(elephant_valve)
    open_valves = open_valves | valves_to_open
    candidate_valves = candidate_valves - valves_to_open

    if remaining_human_minute == 0 and remaining_elephant_minute == 0 and len(candidate_valves) == 1:
        elephant_valve = None
        remaining_elephant_minute = 999_999

    flow_for_this_minute = sum([valve.flow_rate for valve in open_valves])
    max_flow_from_this_minute_onward = flow_for_this_minute * (TIME_TO_COMPLETE + 1 - minute)

    if remaining_human_minute == 0 and remaining_elephant_minute == 0:
        for next_human_valve, next_elephant_valve in itertools.permutations(candidate_valves, 2):
            human_time_to_turn_on = human_valve.valve_time_to_turn_on[next_human_valve]
            elephant_time_to_turn_on = elephant_valve.valve_time_to_turn_on[next_elephant_valve]
            time_to_turn_on = min(human_time_to_turn_on, elephant_time_to_turn_on)

            if minute + time_to_turn_on > TIME_TO_COMPLETE:
                continue

            max_flow_after_next_valve_turned_on = max_flow_for_given_minute(
                human_valve=next_human_valve,
                elephant_valve=next_elephant_valve,
                remaining_human_minute=human_time_to_turn_on - time_to_turn_on,
                remaining_elephant_minute=elephant_time_to_turn_on - time_to_turn_on,
                candidate_valves=candidate_valves,
                open_valves=open_valves,
                minute=minute + time_to_turn_on,
            )

            max_flow_from_this_minute_onward = max(
                max_flow_from_this_minute_onward,
                flow_for_this_minute * time_to_turn_on + max_flow_after_next_valve_turned_on,
            )

        return max_flow_from_this_minute_onward

    if remaining_human_minute == 0:
        for next_human_valve in candidate_valves:
            human_time_to_turn_on = human_valve.valve_time_to_turn_on[next_human_valve]
            time_to_turn_on = min(human_time_to_turn_on, remaining_elephant_minute)

            if minute + time_to_turn_on > TIME_TO_COMPLETE:
                continue

            max_flow_after_next_valve_turned_on = max_flow_for_given_minute(
                human_valve=next_human_valve,
                elephant_valve=elephant_valve,
                remaining_human_minute=human_time_to_turn_on - time_to_turn_on,
                remaining_elephant_minute=remaining_elephant_minute - time_to_turn_on,
                candidate_valves=candidate_valves,
                open_valves=open_valves,
                minute=minute + time_to_turn_on,
            )

            max_flow_from_this_minute_onward = max(
                max_flow_from_this_minute_onward,
                flow_for_this_minute * time_to_turn_on + max_flow_after_next_valve_turned_on,
            )

        return max_flow_from_this_minute_onward

    if remaining_elephant_minute == 0:
        for next_elephant_valve in candidate_valves:
            elephant_time_to_turn_on = elephant_valve.valve_time_to_turn_on[next_elephant_valve]
            time_to_turn_on = min(elephant_time_to_turn_on, remaining_human_minute)

            if minute + time_to_turn_on > TIME_TO_COMPLETE:
                continue

            max_flow_after_next_valve_turned_on = max_flow_for_given_minute(
                human_valve=human_valve,
                elephant_valve=next_elephant_valve,
                remaining_human_minute=remaining_human_minute - time_to_turn_on,
                remaining_elephant_minute=elephant_time_to_turn_on - time_to_turn_on,
                candidate_valves=candidate_valves,
                open_valves=open_valves,
                minute=minute + time_to_turn_on,
            )

            max_flow_from_this_minute_onward = max(
                max_flow_from_this_minute_onward,
                flow_for_this_minute * time_to_turn_on + max_flow_after_next_valve_turned_on,
            )

        return max_flow_from_this_minute_onward

    raise Exception(f"Unexpected remaining_elephant_minute is {remaining_elephant_minute} and remaining_human_minute is {remaining_human_minute} at minute {minute}")


def start_execution(
        candidate_valves: List[Valve],
        first_valve: Valve,
        human_valve: Valve,
        elephant_valve: Valve,
):
    human_time_to_turn_on = first_valve.valve_time_to_turn_on[human_valve]
    elephant_time_to_turn_on = first_valve.valve_time_to_turn_on[elephant_valve]
    time_to_turn_on = min(human_time_to_turn_on, elephant_time_to_turn_on)
    return max_flow_for_given_minute(
        human_valve=human_valve,
        elephant_valve=elephant_valve,
        remaining_human_minute=human_time_to_turn_on - time_to_turn_on,
        remaining_elephant_minute=elephant_time_to_turn_on - time_to_turn_on,
        candidate_valves=candidate_valves,
        open_valves=set(),
        minute=time_to_turn_on + 1,
    )


def main():
    valves = read_valves()
    populate_valve_time_to_turn_on(set(valves))
    candidate_valves = set(valves[0].valve_time_to_turn_on.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [
            executor.submit(start_execution,
                            candidate_valves,
                            valves[0],
                            human_valve,
                            elephant_valve)
            for human_valve, elephant_valve
            in itertools.combinations(candidate_valves, 2)
        ]
        print(max([future.result() for future in concurrent.futures.as_completed(futures)]))


if __name__ == '__main__':
    main()
