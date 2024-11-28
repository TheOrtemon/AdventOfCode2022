from collections import deque
from dataclasses import dataclass
test_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

@dataclass
class Step:
    coords: tuple[int, int]
    priority: int
    
    def __lt__(self, other):
        return self.priority < other.priority

def get_ord(c: str) -> int:
    match c:
        case "S":
            return ord("a")
        case "E":
            return ord("z")
        case _:
            return ord(c)

# lines = test_input.splitlines()
lines = open("input.txt", "r").read().splitlines()

matrix = [[c for c in line] for line in lines]



DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def solve():
    start = None
    for y, line in enumerate(matrix):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                break
    assert start is not None
    been = set(start)
    q = deque()
    q.append(Step(start, 0))
    while q:
        step = q.popleft()
        (x, y), priority = step.coords, step.priority
        next_priority = priority + 1
        # print(x, y, priority)
        for (dx, dy) in DIRECTIONS:
            xi, yi = x + dx, y + dy
            if 0 <= xi < len(matrix[0]) and 0 <= yi < len(matrix):
                dest = matrix[yi][xi]
                cur = matrix[y][x]
                if dest == "E" and cur in ["z", "y"]:
                    print("res", next_priority)
                    return
                diff = get_ord(dest) - get_ord(cur) 
                if diff < 2 and (xi, yi) not in been:
                    new_step = Step((xi, yi), next_priority)
                    been.add((xi, yi))
                    q.append(new_step)

def solve2():
    start = None
    for y, line in enumerate(matrix):
        for x, c in enumerate(line):
            if c == "E":
                start = (x, y)
                break
    assert start is not None
    been = set(start)
    q = deque()
    q.append(Step(start, 0))
    while q:
        step = q.popleft()
        (x, y), priority = step.coords, step.priority
        next_priority = priority + 1
        # print(x, y, priority)
        for (dx, dy) in DIRECTIONS:
            xi, yi = x + dx, y + dy
            if 0 <= xi < len(matrix[0]) and 0 <= yi < len(matrix):
                dest = matrix[yi][xi]
                cur = matrix[y][x]
                if dest == "a" and cur == "b":
                    print("res 2 ", next_priority)
                    return
                diff = get_ord(dest) - get_ord(cur) 
                if diff >= -1 and (xi, yi) not in been:
                    new_step = Step((xi, yi), next_priority)
                    been.add((xi, yi))
                    q.append(new_step)

solve()
solve2()
