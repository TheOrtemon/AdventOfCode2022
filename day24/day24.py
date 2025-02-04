from enum import Enum, auto
import os
import sys
from collections import deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from coordinate import Coordinate, Direction

input = open("input.txt", "r").read()
# input = open("test_input.txt", "r").read().strip()


starting_grid = [list(line) for line in input.splitlines()]
HEIGHT, WIDTH = len(starting_grid), len(starting_grid[0])
START = Coordinate(1, 0)
END = Coordinate(WIDTH - 2, HEIGHT - 1)

dirs = [Direction.up, Direction.down, Direction.left, Direction.right, Coordinate(0, 0)]

def arrow_to_char(arrow):
    match arrow:
        case "<":
            return "W"
        case ">":
            return "E"
        case "^":
            return "N"
        case "v":
            return "S"
        case _:
            return arrow

def move_one_cell(new_grid, coord, dir):
    new_coord = coord + dir
    new_value = new_coord.get_value_from_grid(new_grid)
    if new_value == "#" or new_coord == START or new_coord == END:
        newest_coord = new_coord + dir
        moded_coord = Coordinate(newest_coord.x % WIDTH, newest_coord.y % HEIGHT)
        move_one_cell(new_grid, moded_coord, dir)
        return
    match (dir.x, dir.y):
        case (0, 1):
            match new_value:
                case ".":
                    new_grid[new_coord.y][new_coord.x] = "v"
                case _:
                    new_grid[new_coord.y][new_coord.x] = arrow_to_char(new_value) + "S"
        case (0, -1):
            match new_value:
                case ".":
                    new_grid[new_coord.y][new_coord.x] = "^"
                case _:
                    new_grid[new_coord.y][new_coord.x] = arrow_to_char(new_value) + "N"
        case (-1, 0):
            match new_value:
                case ".":
                    new_grid[new_coord.y][new_coord.x] = "<"
                case _:
                    new_grid[new_coord.y][new_coord.x] = arrow_to_char(new_value) + "W"
        case (1, 0):
            match new_value:
                case ".":
                    new_grid[new_coord.y][new_coord.x] = ">"
                case _:
                    new_grid[new_coord.y][new_coord.x] = arrow_to_char(new_value) + "E"
        case _:
            raise Exception("Unreachable")


def run_blizzard(grid):
    new_grid = [list() for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            old_char = grid[y][x]
            new_char = "#" if old_char == "#" else "."
            new_grid[y].append(new_char)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cur_coord = Coordinate(x, y)
            cur_char = cur_coord.get_value_from_grid(grid)
            if cur_char == "v" or "S" in cur_char:
                move_one_cell(new_grid, cur_coord, Direction.down)
            if cur_char == "^" or "N" in cur_char:
                move_one_cell(new_grid, cur_coord, Direction.up)
            if cur_char == ">" or "E" in cur_char:
                move_one_cell(new_grid, cur_coord, Direction.right)
            if cur_char == "<" or "W" in cur_char:
                move_one_cell(new_grid, cur_coord, Direction.left)
    return new_grid

class Goal(Enum):
    end = auto()
    snack = auto()
    ret = auto()


def solve(is_part2 = False):
    start_pos: tuple[Coordinate, int, Goal] = (START, 0, Goal.end)
    been = set([start_pos])
    q = deque([start_pos])
    grid = starting_grid
    cur_bliz_step = 0
    while True:
        cur_coord, cur_step, goal = q.popleft()
        new_goal = goal.__copy__()
        if not is_part2:
            if cur_coord == END:
                return cur_step
        elif goal == Goal.end and cur_coord == END:
            new_goal = Goal.snack
        elif goal == Goal.snack and cur_coord == START:
            new_goal = Goal.ret
        elif goal == Goal.ret and cur_coord == END:
            return cur_step
        if cur_bliz_step == cur_step:
            grid = run_blizzard(grid)
            # print("\n".join("".join(line) for line in grid))
            # print()
            cur_bliz_step += 1
        new_step = cur_step + 1
        for dir in dirs:
            new_coord: Coordinate = dir + cur_coord
            new_pos = (new_coord, new_step, new_goal)
            new_floor = new_coord.get_value_from_grid(grid)
            if new_floor == "." and new_pos not in been:
                q.append(new_pos)
                been.add(new_pos)

res1 = solve()
print(f"{res1=}")
res2 = solve(is_part2=True)
print(f"{res2=}")


