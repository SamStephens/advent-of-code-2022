#!/usr/bin/env python3

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import List, Callable
import re


@dataclass
class Monkey:
    number: int
    items: List[int]
    operation: Callable[[int], int]
    test_divisible_by: int
    monkey_if_true: int
    monkey_if_false: int
    inspect_count: int = field(default_factory=int)

    def throw_items(self, monkeys: dict[int, Monkey], combined_modulo) -> int:
        items = self.items
        self.items = []
        self.inspect_count += len(items)
        for item in items:
            item = self.operation(item)
            # This is how we keep our numbers reasonably bounded
            item = item % combined_modulo
            if item % self.test_divisible_by == 0:
                monkeys[self.monkey_if_true].receive_item(item)
            else:
                monkeys[self.monkey_if_false].receive_item(item)

    def receive_item(self, item: int) -> None:
        self.items.append(item)


def multiply_operation(multiply_value):
    return lambda old: old * multiply_value


def add_operation(add_value):
    return lambda old: old + add_value


def read_monkeys() -> dict[int, Monkey]:
    monkeys = {}
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        number = int(re.match('Monkey (\\d)+:', line).group(1))

        line = sys.stdin.readline().strip('\n')
        items = line[18:].split(', ')
        items = [int(item) for item in items]

        line = sys.stdin.readline().strip('\n')
        operation_string = line[19:]
        if operation_string == 'old * old':
            operation = lambda old: old * old
        elif operation_string.startswith('old * '):
            multiply_value = int(operation_string.split(' * ')[1])
            operation = multiply_operation(multiply_value)
        else:
            add_value = int(operation_string.split(' + ')[1])
            operation = add_operation(add_value)

        line = sys.stdin.readline().strip('\n')
        test_divisible_by = int(line[21:])

        line = sys.stdin.readline().strip('\n')
        monkey_if_true = int(line[29:])

        line = sys.stdin.readline().strip('\n')
        monkey_if_false = int(line[30:])

        line = sys.stdin.readline().strip('\n')
        monkeys[number] = Monkey(
            number=number,
            items=items,
            operation=operation,
            test_divisible_by=test_divisible_by,
            monkey_if_true=monkey_if_true,
            monkey_if_false=monkey_if_false,
        )

    return monkeys


def main():
    monkeys = read_monkeys()

    sorted_monkeys = [monkeys[key] for key in sorted(monkeys.keys())]
    combined_modulo = math.prod([monkey.test_divisible_by for monkey in sorted_monkeys])

    for _ in range(10_000):
        for monkey in sorted_monkeys:
            monkey.throw_items(monkeys, combined_modulo)

    inspect_counts = [monkey.inspect_count for monkey in sorted_monkeys]
    top1, top2 = sorted(inspect_counts)[-2:]
    print(top1 * top2)


if __name__ == '__main__':
    main()
