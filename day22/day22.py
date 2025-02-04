import os
import re
import sys

from coordinate import Coordinate, Direction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


input = open("input.txt", "r").read()
# input = open("test_input.txt", "r").read()

re_pattern = r"\d+|[RL]"

grid_str, path_str = input.split("\n\n")
grid = [list(line) for line in grid_str.splitlines()]
path = re.findall(re_pattern, path_str)
HEIGHT, WIDTH = grid.__len__(), grid[0].__len__()
QUANT = HEIGHT // 4

assert HEIGHT / 4 == WIDTH / 3 == QUANT


start_x = (i for (i, char) in enumerate(grid[0]) if char == ".").__next__()
start_point = Coordinate(start_x, 0)

#     eeeEgggG
#    F........c
#    f........c
#    f........c
#    f........C
#    A....bbbB
#    a....b
#    a....b
# Aaaa....B
#f........C
#f........c
#f........c
#F........c
#e....dddD
#e....d
#e....d
#E....D
# gggG

def get_next_point(cur_point: Coordinate, cur_dir, grid, n, is_part2 = False) -> tuple[Coordinate, Direction, int]:
    new_point: Coordinate = cur_point + cur_dir
    new_value = new_point.get_value_from_grid(grid)
    match new_value:
        case None | " ":
            if is_part2:
                if cur_dir == Direction.up:
                    match cur_point.x // QUANT:
                        case 0: # a
                            new_dir = Direction.right
                            new_point = Coordinate(QUANT, QUANT + cur_point.x)
                        case 1: # e
                            new_dir = Direction.right
                            new_point = Coordinate(0, QUANT * 2 + cur_point.x)
                        case 2: # g
                            new_dir = cur_dir
                            new_point = Coordinate(cur_point.x - QUANT * 2, QUANT * 4 - 1)
                elif cur_dir == Direction.down:
                    match cur_point.x // QUANT:
                        case 0: # g
                            new_dir = cur_dir
                            new_point = Coordinate(cur_point.x + QUANT * 2, 0)
                        case 1: # d
                            new_dir = Direction.left
                            new_point = Coordinate(QUANT - 1, QUANT * 2 + cur_point.x)
                        case 2: # b
                            new_dir = Direction.left
                            new_point = Coordinate(QUANT * 2 - 1, cur_point.x - QUANT)
                elif cur_dir == Direction.left:
                    match cur_point.y // QUANT:
                        case 0: # f
                            new_dir = Direction.right
                            new_point = Coordinate(0, QUANT * 3 - cur_point.y - 1)
                        case 1: # a
                            new_dir = Direction.down
                            new_point = Coordinate(cur_point.y - QUANT , QUANT * 2)
                        case 2: # f
                            new_dir = Direction.right
                            new_point = Coordinate(QUANT, QUANT * 3 - cur_point.y - 1)
                        case 3: # e
                            new_dir = Direction.down
                            new_point = Coordinate(cur_point.y - QUANT * 2, 0)
                elif cur_dir == Direction.right:
                    match cur_point.y // QUANT:
                        case 0: # c
                            new_dir = Direction.left
                            new_point = Coordinate(QUANT * 2 - 1, QUANT * 3 - cur_point.y - 1)
                        case 1: # b
                            new_dir = Direction.up
                            new_point = Coordinate(cur_point.y + QUANT, QUANT - 1)
                        case 2: # c
                            new_dir = Direction.left
                            new_point = Coordinate(QUANT * 3 - 1, QUANT * 3 - cur_point.y - 1)
                        case 3: # d
                            new_dir = Direction.up
                            new_point = Coordinate(cur_point.y - QUANT * 2, QUANT * 3 - 1)

                new_value = new_point.get_value_from_grid(grid)
                match new_value:
                    case ".":
                        return new_point, new_dir, n - 1
                    case "#":
                        return cur_point, cur_dir, 0
                    case _:
                        assert False, (cur_point.x, cur_point.y, new_point.x, new_point.y, new_value)

            while True:
                if new_value is None:
                    new_point = new_point + cur_dir.turn_left().turn_left()
                new_point = new_point.wrapping_add(cur_dir, grid)
                new_value = new_point.get_value_from_grid(grid)
                if new_value in [".", "#"]:
                    match new_value:
                        case ".":
                            return new_point, cur_dir, n - 1
                        case "#":
                            return new_point, cur_dir, 0
        case ".":
            return new_point, cur_dir, n - 1
        case "#":
            return cur_point, cur_dir, 0
    raise Exception("Unrechable")


def solve(is_part2 = False):
    cur_dir: Direction = Direction.right
    cur_point = start_point
    for n in path:
        match n:
            case "L":
                cur_dir = cur_dir.turn_left()
                continue
            case "R":
                cur_dir = cur_dir.turn_right()
                continue
            case _:
                n = int(n)
        while n > 0:
            new_point, new_dir, new_n = get_next_point(cur_point, cur_dir, grid, n, is_part2 = is_part2)
            value = new_point.get_value_from_grid(grid)
            cur_point = new_point
            cur_dir = new_dir
            n = new_n
    return (cur_point.x + 1) * 4 + (cur_point.y + 1) * 1000 + get_dir_index(cur_dir)

def get_dir_index(dir):
    match (dir.x, dir.y):
        case (1, 0):
            return 0
        case (0, 1):
            return 1
        case (-1, 0):
            return 2
        case (0, -1):
            return 3
        case _:
            raise Exception("Unrechable")

res1 = solve()
res2 = solve(is_part2=True)
print(f"{res1=}")
print(f"{res2=}")
