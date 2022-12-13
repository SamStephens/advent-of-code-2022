#!/usr/bin/env python3

import ast
import sys


def normalise(list_left, list_right):
    """
    Recursively ensure that matching elements in the two packets are both packets if either are, by converting any non-list
    elements into a singleton list.
    """
    for index in range(min(len(list_left), len(list_right))):
        if type(list_left[index]) is list and type(list_right[index]) is not list:
            list_right[index] = [list_right[index]]
        if type(list_right[index]) is list and type(list_left[index]) is not list:
            list_left[index] = [list_left[index]]
        if type(list_left[index]) is list:
            normalise(list_left[index], list_right[index])


def main():
    index_sum = 0
    index = 1
    while True:
        line_left = sys.stdin.readline().strip('\n')
        if not line_left:
            break

        line_right = sys.stdin.readline().strip('\n')
        sys.stdin.readline()

        list_left = ast.literal_eval(line_left)
        list_right = ast.literal_eval(line_right)

        normalise(list_left, list_right)

        if list_left <= list_right:
            index_sum += index

        index += 1

    print(index_sum)


if __name__ == '__main__':
    main()
