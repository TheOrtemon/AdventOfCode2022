from enum import Enum, auto
from itertools import cycle
from typing import List, Tuple
from dataclasses import dataclass

input = open("input.txt", "r").read().strip()
# input = open("test_input.txt", "r").read().strip()

type Coord = Tuple[int, int]
WIDTH = 7

class FigureType(Enum):
    Minus = auto()
    Plus = auto()
    Angle = auto()
    Pipe = auto()
    Square = auto()

@dataclass
class Figure:
    base: Coord
    block: List[Coord]
    type: FigureType

    def is_impossible(self, board, cur_base: Coord | None = None) -> bool:
        if cur_base is None:
            cur_base = self.base
        for rel_pos in self.block:
            pos = add_tuples(rel_pos, cur_base)
            if pos[0] < 0 or pos[0] >= WIDTH or pos[1] < 0:
                return True
            if pos in board:
                return True
        return False

    def add_on_board(self, board):
        for rel_pos in self.block:
            pos = add_tuples(rel_pos, self.base)
            board.add(pos)

    def has_moved(self, board, dir) -> bool:
        match dir:
            case ">":
                new_base = (self.base[0] + 1, self.base[1])
                if not self.is_impossible(board, new_base):
                    self.base = new_base
                    return True
            case "<":
                new_base = (self.base[0] - 1, self.base[1])
                if not self.is_impossible(board, new_base):
                    self.base = new_base
                    return True
            case "v":
                new_base = (self.base[0], self.base[1] - 1)
                if not self.is_impossible(board, new_base):
                    self.base = new_base
                    return True
        return False

    def highest_point(self) -> int:
        max_y = 0
        for rel_pos in self.block:
            pos = add_tuples(rel_pos, self.base)
            max_y = max(max_y, pos[1])
        return max_y


def new_figure(cur_height, figures) -> Figure:
    base = (2, cur_height + 3)
    match next(figures):
        case FigureType.Minus:
            return Figure(base, [(0, 0), (1, 0), (2, 0), (3, 0)], FigureType.Minus)
        case FigureType.Plus:
            return Figure(base, [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1)], FigureType.Plus)
        case FigureType.Angle:
            return Figure(base, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], FigureType.Angle)
        case FigureType.Pipe:
            return Figure(base, [(0, 0), (0, 1), (0, 2), (0, 3)], FigureType.Pipe)
        case FigureType.Square:
            return Figure(base, [(0, 0), (1, 0), (0, 1), (1, 1)], FigureType.Square)

def add_tuples(self: Coord, other: Coord) -> Coord:
    return (self[0] + other[0], self[1] + other[1])

def solve(rocks) -> int:
    memory = dict()
    board: set[Coord] = set()
    cur_rock = 0
    cur_height = 0
    dirs = cycle(input)
    figures = cycle([FigureType.Minus, 
                    FigureType.Plus, 
                    FigureType.Angle, 
                    FigureType.Pipe, 
                    FigureType.Square])
    while cur_rock <= rocks:
        is_bottom = False
        figure = new_figure(cur_height, figures)
        while not is_bottom:
            dir = next(dirs)
            figure.has_moved(board, dir)
            has_moved_down = figure.has_moved(board, "v")
            if not has_moved_down:
                figure.add_on_board(board)
                cur_rock += 1
                is_bottom = True
                cur_height = max(cur_height, figure.highest_point() + 1)
                memory[cur_rock] = cur_height
                if cur_rock < input.__len__() + 1:
                    continue
                max_period = (cur_rock - 5) // 3
                for pot_period in range(5, max_period):
                    d1 = memory[cur_rock] - memory[cur_rock - pot_period]
                    d2 = memory[cur_rock - pot_period] - memory[cur_rock - 2 * pot_period]
                    d3 = memory[cur_rock - 2 * pot_period] - memory[cur_rock - 3 * pot_period]
                    di1 = memory[cur_rock - 1] - memory[cur_rock - 1 - pot_period]
                    di2 = memory[cur_rock - 1 - pot_period] - memory[cur_rock - 1 - 2 * pot_period]
                    di3 = memory[cur_rock - 1 - 2 * pot_period] - memory[cur_rock - 1 - 3 * pot_period]
                    dj1 = memory[cur_rock - 2] - memory[cur_rock - 2 - pot_period]
                    dj2 = memory[cur_rock - 2 - pot_period] - memory[cur_rock - 2 - 2 * pot_period]
                    dj3 = memory[cur_rock - 2 - 2 * pot_period] - memory[cur_rock - 2 - 3 * pot_period]
                    dk1 = memory[cur_rock - 3] - memory[cur_rock - 3 - pot_period]
                    dk2 = memory[cur_rock - 3 - pot_period] - memory[cur_rock - 3 - 2 * pot_period]
                    dk3 = memory[cur_rock - 3 - 2 * pot_period] - memory[cur_rock - 3 - 3 * pot_period]
                    if d1 == d2 == d3 == di1 == di2 == di3 == dj1 == dj2 == dj3 == dk1 == dk2 == dk3:
                        cycles = 1 + (rocks - cur_rock) // pot_period
                        last_known_rock = rocks - pot_period * cycles
                        return memory[last_known_rock] + cycles * d1

    return cur_height - 2

print("res1 = ", solve(2022))
print("res2 = ", solve(1000000000000))

