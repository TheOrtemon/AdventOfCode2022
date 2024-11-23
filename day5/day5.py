from copy import deepcopy
test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

f = open("input.txt", "r")
lines = f.readlines()
f.close()

# lines = test_input.splitlines()

split_index = lines.index("\n")
cargos = lines[:split_index]
moves = lines[split_index + 1:]

cargo_lines = []
for cargo_line in cargos:
    cargo_list = []
    # print(cargo_line)
    for i in range(0, cargo_line.__len__(), 4):
        cargo_box = cargo_line[i:i+4]
        cargo_str = cargo_box.strip().strip("[]")
        cargo = cargo_str or None
        # print(cargo)
        cargo_list.append(cargo)
    cargo_lines.append(cargo_list)

cargo_lines = cargo_lines[:-1]

vertical_lines = []

for c in range(len(cargo_lines[0])):
    vertical_lines.append([])
    for l in range(len(cargo_lines) -1, -1, -1):
        if box := cargo_lines[l][c]:
            vertical_lines[-1].append(box)

vertical_lines2 = deepcopy(vertical_lines)

for move_line in moves:
    i, rest = move_line[5:].split(" ", 1) 
    frm, rest = rest[5:].split(" ", 1)
    to = rest[3:]
    i, frm, to = int(i), int(frm), int(to)
    for _ in range(i):
        cur_box = vertical_lines[frm - 1].pop()
        vertical_lines[to - 1].append(cur_box)

    # print(vertical_lines2)
    cur_slice = vertical_lines2[frm - 1][-i:]
    # print(cur_slice, i)
    vertical_lines2[to - 1] += cur_slice 
    vertical_lines2[frm - 1] = vertical_lines2[frm - 1][:-i]

print(vertical_lines)
print(vertical_lines2)

res = "".join(l[-1] if l else "" for l in vertical_lines)
print(res)

res2 = "".join(l[-1] if l else "" for l in vertical_lines2)
print(res2)
