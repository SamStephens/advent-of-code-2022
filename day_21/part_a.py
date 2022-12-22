#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Any


@dataclass
class Node:
    def evaluate(self):
        raise NotImplementedError


@dataclass
class Value:
    value: int

    def evaluate(self):
        return self.value


@dataclass
class Operation:
    operand_1: Node
    operand_2: Node
    operator: str

    def evaluate(self):
        if self.operator == '+':
            return self.operand_1.evaluate() + self.operand_2.evaluate()
        if self.operator == '-':
            return self.operand_1.evaluate() - self.operand_2.evaluate()
        if self.operator == '*':
            return self.operand_1.evaluate() * self.operand_2.evaluate()
        if self.operator == '/':
            return self.operand_1.evaluate() // self.operand_2.evaluate()
        raise ValueError(f"Unexpected operator {self.operator}")


def build_node(nodes, name):
    node = nodes[name]
    if type(node) is int:
        return Value(value=node)

    operand_1, operand_2, operator = node
    return Operation(
        operand_1=build_node(nodes, operand_1),
        operand_2=build_node(nodes, operand_2),
        operator=operator,
    )


def main():
    nodes: Dict[str, Any] = dict()

    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        match = re.fullmatch(
            "([a-z]+): (\\d+)",
            line,
        )

        if match:
            name, value = match.groups()
            value = int(value)
            nodes[name] = value
            continue

        match = re.fullmatch(
            "([a-z]+): ([a-z]+) ([-+/*]) ([a-z]+)",
            line,
        )

        if match:
            name, operand_1, operator, operand_2 = match.groups()
            nodes[name] = operand_1, operand_2, operator,
            continue

        raise ValueError(f"Unexpected line {line}")

    root = build_node(nodes, "root")
    print(root.evaluate())


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
