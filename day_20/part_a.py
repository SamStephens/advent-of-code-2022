#!/usr/bin/env python3

from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple


@dataclass
class ListNode:
    value: int
    previous: ListNode
    next: ListNode


def read_elements() -> Tuple[ListNode, List[ListNode]]:
    zero_element: ListNode = None
    previous: ListNode = None
    elements: List[ListNode] = []
    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        value = int(line) * 811589153
        element = ListNode(
            value,
            previous,
            None,
        )
        if value == 0:
            zero_element = element

        if previous is not None:
            previous.next = element

        elements.append(element)
        previous = element

    first = elements[0]
    last = elements[-1]
    first.previous = last
    last.next = first

    return zero_element, elements


def print_list(first_element):
    e = first_element
    while True:
        print(e.value)
        e = e.next
        if e == first_element:
            break


def main():
    zero_element, elements = read_elements()
    length_less_one_element = len(elements) - 1

    for _ in range(10):
        for element in elements:
            previous = element.previous
            next = element.next
            previous.next = next
            next.previous = previous

            if element.value >= 0:
                for _ in range(element.value % length_less_one_element):
                    previous = previous.next
            else:
                for _ in range(abs(element.value % length_less_one_element)):
                    previous = previous.previous

            next = previous.next
            previous.next = element
            element.previous = previous
            element.next = next
            next.previous = element

    element = zero_element

    for _ in range(1000):
        element = element.next
        number_1000 = element.value

    for _ in range(1000):
        element = element.next
        number_2000 = element.value

    for _ in range(1000):
        element = element.next
        number_3000 = element.value

    print(number_1000 + number_2000 + number_3000)


if __name__ == '__main__':
    # import cProfile
    # import re
    #
    # cProfile.run('main()')
    main()
