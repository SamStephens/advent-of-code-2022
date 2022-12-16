#!/usr/bin/env python3

from __future__ import annotations
import itertools
import sys
import re
from dataclasses import dataclass
from typing import List, Set
from collections import defaultdict

from aws_cdk.aws_stepfunctions import Map


@dataclass
class Valve:
    name: str
    flow_rate: int
    linked_valves: List[Valve]

    def __hash__(self):
        return hash(self.name)

def read_valves() -> List[Valve]:
    valves = {}
    valve_linkages: Map[str, Valve] = {}
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
        )
        valve_linkages[valve_name] = linked_valve_names

    for valve in valves.values():
        linked_valves = valve_linkages[valve.name]
        linked_valves = [valves[valve_name] for valve_name in linked_valves]
        valve.linked_valves = linked_valves

    valves = list(valves.values())
    valves.sort(key=lambda v: v.name)
    return valves


def max_flow_for_given_minute(
        current_valve: Valve,
        all_openable_valves: Set[Valve],
        candidate_openable_valves: Set[Valve],
        visited_since_last_opening: Set[Valve],
        open_valves: Set[Valve],
        minute: int) -> int:
    flow_for_this_minute = sum([valve.flow_rate for valve in open_valves])
    if minute == 30:
        return flow_for_this_minute

    flow_with_no_more_openings = flow_for_this_minute * (31 - minute)
    if not candidate_openable_valves:
        return flow_with_no_more_openings

    candidate_max_flows_from_this_minute_onward = [flow_with_no_more_openings]

    if current_valve.flow_rate > 0 and current_valve not in open_valves:
        flow_for_subsequent_minutes_with_valve_open = max_flow_for_given_minute(
            current_valve=current_valve,
            all_openable_valves=all_openable_valves,
            candidate_openable_valves=candidate_openable_valves - {current_valve, },
            visited_since_last_opening=set(),
            open_valves=open_valves | {current_valve, },
            minute=minute + 1,
        )
        candidate_max_flows_from_this_minute_onward = [
            flow_for_this_minute + flow_for_subsequent_minutes_with_valve_open,
        ]
        max_openable_flow_rate = max([valve.flow_rate for valve in candidate_openable_valves])
        if max_openable_flow_rate < (current_valve.flow_rate * 2):
            # Optimisation - we know we get more flow rate opening this now than opening any other valve sooner.
            return candidate_max_flows_from_this_minute_onward[0]

    flow_for_subsequent_minutes_for_each_linked_valve = [
        max_flow_for_given_minute(
            current_valve=next_value,
            all_openable_valves=all_openable_valves,
            candidate_openable_valves=candidate_openable_valves,
            visited_since_last_opening=visited_since_last_opening | {next_value, },
            open_valves=open_valves,
            minute=minute + 1,
        )
        for next_value
        in current_valve.linked_valves
        if next_value not in visited_since_last_opening
    ]

    candidate_max_flows_from_this_minute_onward += [
        flow_for_this_minute + subsequent_flow
        for subsequent_flow
        in flow_for_subsequent_minutes_for_each_linked_valve
    ]

    return max(candidate_max_flows_from_this_minute_onward)


def main():
    valves = read_valves()
    max_flow_rate = max_flow_for_given_minute(
        current_valve=valves[0],
        all_openable_valves=set([v for v in valves if v.flow_rate > 0]),
        candidate_openable_valves=set([v for v in valves if v.flow_rate > 0]),
        visited_since_last_opening=set(),
        open_valves=set(),
        minute=1,
    )
    print(max_flow_rate)


if __name__ == '__main__':
    main()
