from collections import defaultdict
import sys

MARKER_LENGTH = 14

line = sys.stdin.readline().strip('\n')
index = 0
while True:
    chars = line[index:(index + MARKER_LENGTH)]
    if len(set(chars)) == MARKER_LENGTH:
        print(index + MARKER_LENGTH)
        break
    index += 1
