test_input = """30373
25512
65332
33549
35390"""

# input = test_input.splitlines()
input = open("input.txt", "r").read().splitlines()

H, L = input.__len__(), input[0].__len__()

vis_map = [[False for _ in range(L)] for _ in range(H)]

for y in range(H):
    highest = -1
    for x in range(L):
        if (cur := int(input[y][x])) > highest:
            highest = cur
            vis_map[y][x] = True

for y in range(H):
    highest = -1
    for x in range(L).__reversed__():
        if (cur := int(input[y][x])) > highest:
            highest = cur
            vis_map[y][x] = True

for x in range(L):
    highest = -1
    for y in range(H):
        if (cur := int(input[y][x])) > highest:
            highest = cur
            vis_map[y][x] = True

for x in range(L):
    highest = -1
    for y in range(H).__reversed__():
        if (cur := int(input[y][x])) > highest:
            highest = cur
            vis_map[y][x] = True

res2 = 0
for y in range(H): # part 2
    for x in range(L):
        cur_height = int(input[y][x])
        xr = 0
        for xi in range(x + 1, L):
            xr += 1
            if int(input[y][xi]) >= cur_height:
                break
        xl = 0
        for xi in range(x).__reversed__():
            xl += 1
            if int(input[y][xi]) >= cur_height:
                break
        yd = 0
        for yi in range(y + 1, H):
            yd += 1
            if int(input[yi][x]) >= cur_height:
                break
        yu = 0
        for yi in range(y).__reversed__():
            yu += 1
            if int(input[yi][x]) >= cur_height:
                break
        res2 = max(res2, xr * xl * yu * yd)

res1 = sum(sum(row) for row in vis_map)
print(res1)
print(res2)
