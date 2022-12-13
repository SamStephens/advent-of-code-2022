#!/usr/bin/env python3

import ast
import sys

FIRST_DIVIDER_PACKET = [[2]]
SECOND_DIVIDER_PACKET = [[6]]


def normalise(packets):
    """
    Recursively ensure that matching elements in the packets are all packets if any are, by converting any non-list
    elements into a singleton list.
    """
    for index in range(max([len(packet) for packet in packets])):
        packets_with_element = [packet for packet in packets if len(packet) > index]
        any_is_list = any([type(packet[index]) is list for packet in packets_with_element])
        if any_is_list:
            for packet in packets_with_element:
                if type(packet[index]) is not list:
                    packet[index] = [packet[index]]
            elements = [packet[index] for packet in packets_with_element]
            normalise(elements)


def main():
    packets = []
    while True:
        line = sys.stdin.readline()
        if line == '':
            break

        line = line.strip()
        if not line:
            continue

        packets.append(ast.literal_eval(line))

    packets.append(FIRST_DIVIDER_PACKET)
    packets.append(SECOND_DIVIDER_PACKET)
    normalise(packets)

    packets.sort()
    print((packets.index(FIRST_DIVIDER_PACKET) + 1) * (packets.index(SECOND_DIVIDER_PACKET) + 1))


if __name__ == '__main__':
    main()
