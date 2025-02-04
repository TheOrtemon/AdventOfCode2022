import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from coordinate import Coordinate, Direction

input = open("input.txt", "r").read()
# input = open("test_input.txt", "r").read().strip()


def is_alone(x, y, grid):
    for xi in range(x - 1, x + 2):
        for yi in range(y - 1, y + 2):
            if x != xi or y != yi:
                if Coordinate(xi, yi) in grid:
                    return False
    return True

def solve(is_part2 = False):
    ROUND1 = 10
    grid_matrix = [list(line) for line in input.splitlines()]
    grid = set()
    for (y, line) in enumerate(grid_matrix):
        for (x, c) in enumerate(line):
            if c == "#":
                grid.add(Coordinate(x, y))
    res = 0
    dirs = [Direction.up, Direction.down, Direction.left, Direction.right]
    if not is_part2:
        for _ in range(ROUND1):
            grid, dirs, _ = loop(grid, dirs)
        min_x, max_x, min_y, max_y = 2**62, -(2**62), 2**62, -(2**62)
        for coord in grid:
            min_x = min(min_x, coord.x)
            max_x = max(max_x, coord.x)
            min_y = min(min_y, coord.y)
            max_y = max(max_y, coord.y)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if Coordinate(x, y) not in grid:
                    res += 1
    else:
        is_changing = True
        res = 0
        while is_changing:
            grid, dirs, is_changing = loop(grid, dirs)
            res += 1

    return res

def loop(grid, dirs):
    new_grid = dict()
    is_changing = False
    for cur_coor in grid:
        if is_alone(cur_coor.x, cur_coor.y, grid):
            continue
        for dir in dirs:
            next_coor = dir + cur_coor
            left_neigh = next_coor + dir.turn_left()
            right_neigh = next_coor + dir.turn_right()
            if next_coor in grid or left_neigh in grid or right_neigh in grid:
                continue
            if next_coor not in new_grid:
                new_grid[next_coor] = list()
            new_grid[next_coor].append(cur_coor)
            break
    for key, value in new_grid.items():
        if len(value) == 1:
            is_changing = True
            grid.remove(value[0])
            grid.add(key)
    dirs.append(dirs[0])
    dirs = dirs[1:]
    return grid, dirs, is_changing


res1 = solve()
print(res1)
res2 = solve(is_part2=True)
print(res2)
