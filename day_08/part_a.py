import sys


def visible(tree_height, neighbour_heights):
    return not any([neighbour_height >= tree_height for neighbour_height in neighbour_heights])


grid = []

line = [int(char) for char in sys.stdin.readline().strip('\n')]
while line:
    grid.append(line)
    line = [int(char) for char in sys.stdin.readline().strip('\n')]

visible_count = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        tree_height = grid[y][x]
        left_slice = grid[y][:x]
        right_slice = grid[y][x + 1:]
        top_slice = [row[x] for row in grid[:y]]
        bottom_slice = [row[x] for row in grid[y + 1:]]

        if visible(tree_height, left_slice) or \
                visible(tree_height, right_slice) or \
                visible(tree_height, top_slice) or \
                visible(tree_height, bottom_slice):
            visible_count += 1

print(visible_count)
