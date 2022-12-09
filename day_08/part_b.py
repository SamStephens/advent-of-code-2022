import sys


def distance_unblocked(tree_height, neighbour_heights):
    for distance, neighbour_height in enumerate(neighbour_heights):
        if neighbour_height >= tree_height:
            return distance + 1
    return len(neighbour_heights)


grid = []

line = [int(char) for char in sys.stdin.readline().strip('\n')]
while line:
    grid.append(line)
    line = [int(char) for char in sys.stdin.readline().strip('\n')]

max_scenic_score = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        tree_height = grid[y][x]
        left_slice = grid[y][:x]
        left_slice.reverse()
        right_slice = grid[y][x + 1:]
        top_slice = [row[x] for row in grid[:y]]
        top_slice.reverse()
        bottom_slice = [row[x] for row in grid[y + 1:]]

        left_distance_unblocked = distance_unblocked(tree_height, left_slice)
        right_distance_unblocked = distance_unblocked(tree_height, right_slice)
        top_distance_unblocked = distance_unblocked(tree_height, top_slice)
        bottom_distance_unblocked = distance_unblocked(tree_height, bottom_slice)

        scenic_score = left_distance_unblocked * right_distance_unblocked * top_distance_unblocked * bottom_distance_unblocked
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print(max_scenic_score)
