from dataclasses import dataclass

test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

# lines = test_input.splitlines()
lines = open("input.txt", "r").read().splitlines()

@dataclass
class Wall:
    start: tuple[int, int]
    end: tuple[int, int]

walls: list[Wall] = []

max_depth = 0

for line in lines:
    numbers = [list(map(int, coords.split(","))) for coords in line.split(" -> ")]
    for i in range(len(numbers) - 1):
        start = tuple(numbers[i])
        end = tuple(numbers[i + 1])
        max_depth = max(max_depth, start[1], end[1])
        wall = Wall(start, end)
        walls.append(wall)

min_wall, max_wall = 500 -  max_depth - 2, 500 + max_depth + 2
# print(min_wall, max_wall, max_depth)
# print(walls)

matrix = [["."] * (max_wall - min_wall + 1) for _ in range(max_depth + 1)]
max_depth2 = max_depth + 2
matrix2 = [["."] * (max_wall - min_wall + 1) for _ in range(max_depth2 + 1)]

for wall in walls:
    xs, ys = wall.start
    xe, ye = wall.end
    if xs == xe:
        for y in range(min(ys, ye), max(ys, ye) + 1):
            matrix[y][xs - min_wall] = "#"
            matrix2[y][xs - min_wall] = "#"
    elif ys == ye:
        for x in range(min(xs, xe), max(xs, xe) + 1):
            matrix[ys][x - min_wall] = "#"
            matrix2[ys][x - min_wall] = "#"
    else:
        raise Exception("Unreachable")


x_source, y_source = 500 - min_wall, 0
dps = [(0, 1), (-1, 1), (1, 1)]
changing = True
x, y = x_source, y_source

while changing:
    # print("\n".join("".join(line) for line in matrix))
    # print(x, y)
    for dx, dy in dps:
        xi, yi = x + dx, y + dy
        if not (0 <= xi <= (max_wall - min_wall) and 0 <= yi <= max_depth):
            changing = False
            break
        cur = matrix[yi][xi]
        # print("cur ", cur, xi, yi)
        match cur:
            case ".":
                x, y = xi, yi
                break
            case "o" | '#':
                # print("dx and dy: ", dx, dy)
                if dx == 1 and dy == 1:
                    # print("HEEEEY")
                    matrix[y][x] = "o"
                    x, y = x_source, y_source
                continue
            case _:
                raise Exception("Unreachable")

    

# print("\n".join("".join(line) for line in matrix))

acc = 0

for r in matrix:
    for c in r:
        if c == "o":
            acc += 1

print("res 1 = ", acc)


x, y = x_source, y_source
for xf in range(len(matrix2[0])):
    matrix2[max_depth2][xf] = "#"

# print("PART 2")
changing2 = True

while changing2:
    # # print("\n".join("".join(line) for line in matrix2))
    # print(x, y)
    for dx, dy in dps:
        xi, yi = x + dx, y + dy
        if not (0 <= xi <= (max_wall - min_wall) and 0 <= yi <= max_depth2):
            # print(xi, yi)
            break
        cur = matrix2[yi][xi]
        # print("cur ", cur, xi, yi)
        match cur:
            case ".":
                x, y = xi, yi
                changing2 = True
                break
            case "o" | '#':
                # print("wall or sand. dx and dy: ", dx, dy)
                if dx == 1 and dy == 1 and matrix2[y][x] == ".":
                    # print("HEEEEY")
                    matrix2[y][x] = "o"
                    x, y = x_source, y_source
                    changing2 = True
                    break
                changing2 = False
            case _:
                raise Exception("Unreachable")

    

# print("\n".join("".join(line) for line in matrix2))

acc = 0

for r in matrix2:
    for c in r:
        if c == "o":
            acc += 1

print("res 2 = ", acc)
