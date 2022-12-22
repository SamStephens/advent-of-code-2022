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

    def contains_human_node(self):
        raise NotImplementedError

    def human_node_equate_to(self, result):
        raise NotImplementedError


@dataclass
class Value(Node):
    value: int

    def evaluate(self):
        return self.value

    def contains_human_node(self):
        return False


@dataclass
class Human(Node):
    def evaluate(self):
        raise NotImplementedError

    def contains_human_node(self):
        return True

    def human_node_equate_to(self, result):
        return result


@dataclass
class Operation(Node):
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

    def contains_human_node(self):
        return self.operand_1.contains_human_node() or self.operand_2.contains_human_node()

    def human_node_equate_to(self, result):
        if not (self.operand_1.contains_human_node() or self.operand_2.contains_human_node()):
            raise Exception("No human node")

        operand_1_human_node = self.operand_1.contains_human_node()
        if self.operator == '+':
            if operand_1_human_node:
                other = self.operand_2.evaluate()
                return self.operand_1.human_node_equate_to(result - other)
            else:
                other = self.operand_1.evaluate()
                return self.operand_2.human_node_equate_to(result - other)
        if self.operator == '-':
            if operand_1_human_node:
                other = self.operand_2.evaluate()
                return self.operand_1.human_node_equate_to(result + other)
            else:
                other = self.operand_1.evaluate()
                return self.operand_2.human_node_equate_to(other - result)
        if self.operator == '*':
            if operand_1_human_node:
                other = self.operand_2.evaluate()
                return self.operand_1.human_node_equate_to(result // other)
            else:
                other = self.operand_1.evaluate()
                return self.operand_2.human_node_equate_to(result // other)
        if self.operator == '/':
            if operand_1_human_node:
                other = self.operand_2.evaluate()
                return self.operand_1.human_node_equate_to(result * other)
            else:
                other = self.operand_1.evaluate()
                return self.operand_2.human_node_equate_to(other // result)
        raise ValueError(f"Unexpected operator {self.operator}")


@dataclass
class Equality(Node):
    operand_1: Node
    operand_2: Node

    def human_node_to_make_equal(self):
        if self.operand_1.contains_human_node():
            human_node_operand = self.operand_1
            computable_operand = self.operand_2
        else:
            human_node_operand = self.operand_2
            computable_operand = self.operand_1

        equal_to = computable_operand.evaluate()
        return human_node_operand.human_node_equate_to(equal_to)

    def contains_human_node(self):
        return self.operand_1.contains_human_node() or self.operand_2.contains_human_node()


def build_node(nodes, name) -> Node:
    node = nodes[name]
    if name == 'humn':
        return Human()

    if type(node) is int:
        return Value(value=node)

    operand_1, operand_2, operator = node

    if name == 'root':
        return Equality(
            operand_1=build_node(nodes, operand_1),
            operand_2=build_node(nodes, operand_2),
        )

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
    print(root.human_node_to_make_equal())


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
