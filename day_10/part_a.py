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

        new_cycle_number = cycle_number + cost
        new_register_value = register_value + change

        current_sampled_cycle = sampled_cycle(cycle_number)
        new_sampled_cycle = sampled_cycle(new_cycle_number)

        if current_sampled_cycle != new_sampled_cycle:
            if new_sampled_cycle == new_cycle_number:
                signal_strength = new_register_value * new_sampled_cycle
            else:
                signal_strength = register_value * new_sampled_cycle
            signal_strength_sum += signal_strength

        register_value = new_register_value
        cycle_number = new_cycle_number

    print(signal_strength_sum)


if __name__ == '__main__':
    main()
