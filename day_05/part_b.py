from collections import defaultdict
import sys


crate_stacks = defaultdict(list)

while True:
    line = sys.stdin.readline().strip('\n')
    if '[' not in line:
        break

    for index, crate in enumerate(line[1::4]):
        if crate == ' ':
            continue

        crate_stacks[index + 1] = [crate] + crate_stacks[index + 1]

while True:
    line = sys.stdin.readline()
    if line == '':
        break

    if not line.startswith('move '):
        continue

    (_, crate_count, _, from_crate, _, to_crate) = line.strip().split(' ')

    crate_count, from_crate, to_crate = int(crate_count), int(from_crate), int(to_crate)

    crate_stacks[to_crate].extend(crate_stacks[from_crate][-crate_count:])
    del crate_stacks[from_crate][-crate_count:]

result = ''
for index in sorted(crate_stacks.keys()):
    result += crate_stacks[index].pop()

print(result)
