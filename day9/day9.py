from typing import Tuple
input_text = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

lines = open("input.txt", "r").read().splitlines()
# lines = input_text.splitlines()

def dx_to_dxh(p: Tuple[int, int]) -> Tuple[int, int]:
    match p:
        case (0, 2):
            return 0, 1
        case 2, 0:
            return 1, 0
        case 0, -2:
            return 0, -1
        case -2, 0:
            return -1, 0
        case (1, 2) | (2, 1) | (2, 2):
            return 1, 1
        case (-1, 2) | (-2, 1) | (-2, 2):
            return -1, 1
        case (1, -2) | (2, -1) | (2, -2):
            return 1, -1
        case (-1, -2) | (-2, -1) | (-2, -2):
            return -1, -1
        case _:
            raise Exception("Unreachable")

def solve(snake_length, lines):

    snake = [(0, 0)] * snake_length
    next_snake = [(0, 0)] * snake_length
    been = {(0, 0)}

    for line in lines:
        dir, n = (split := line.split())[0], int(split[1])
        match dir:
            case "R":
                dxh, dyh = 1, 0
            case "L":
                dxh, dyh = -1, 0
            case "U":
                dxh, dyh = 0, 1
            case _: # D
                dxh, dyh = 0, -1

        for _ in range(n):
            for i in range(snake_length).__reversed__():
                xt, yt = snake[i]
                if (i + 1) >= snake_length:
                    dx, dy = dxh * 2, dyh * 2
                    xhi, yhi = xt + dx, yt + dy
                else:
                    xhi, yhi = next_snake[i + 1]
                    dx, dy = xhi - xt, yhi - yt
                if abs(xhi - xt) in (1, 0) and abs(yhi - yt) in (1, 0):
                    break
                dx, dy = dx_to_dxh((dx, dy))
                
                next_snake[i] = xt + dx, yt + dy
            snake = next_snake.copy()
            been.add(next_snake[0])
    
    return len(been)

print(solve(2, lines))
print(solve(10, lines))



