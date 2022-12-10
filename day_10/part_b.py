#!/usr/bin/env python3

import sys


def sampled_cycle(cycle_number):
    return ((cycle_number + 20) // 40) * 40 - 20


def main():
    cycle_number = 1
    register_value = 1
    signal_strength_sum = 0

    while True:
        line = sys.stdin.readline().strip('\n')
        if not line:
            break

        if line == 'noop':
            cost = 1
            change = 0
        else:
            cost = 2
            _, change = line.split(' ')
            change = int(change)

        for _ in range(cost):
            x_position = (cycle_number - 1) % 40
            if x_position == 0:
                print()
            if (register_value - 1) <= x_position <= (register_value + 1):
                print('#', end='')
            else:
                print('.', end='')
            cycle_number += 1

        register_value += change

    print()

if __name__ == '__main__':
    main()
