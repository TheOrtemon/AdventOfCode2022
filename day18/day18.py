from collections import deque

input = open("input.txt", "r").read().strip().splitlines()
# input = open("test_input.txt", "r").read().strip().splitlines()

total_area = 0
droplet_set = set()

x_min = y_min = z_min = float("inf")
x_max = y_max = z_max = float("-inf")

def is_in_bound(point):
    (x, y, z) = point
    return x_max >= x >= x_min and y_max >= y >= y_min and z_max >= z >= z_min

def get_neighbours(x, y, z):
    neighbours = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    return neighbours

for line in input:
    pot_area = 0
    x, y, z = (int(n) for n in line.split(","))
    x_max = max(x_max, x + 1)
    y_max = max(y_max, y + 1)
    z_max = max(z_max, z + 1)
    x_min = min(x_min, x - 1)
    y_min = min(y_min, y - 1)
    z_min = min(z_min, z - 1)
    neighbours = get_neighbours(x, y, z)
    for neighbour in neighbours:
        pot_area += 1 if neighbour not in droplet_set else -1
    total_area += pot_area
    droplet_set.add((x, y, z))

start = (x_min, y_min, z_min)
outer_air_set = set([start])
q = deque([start])
outer_area = 0

while len(q) > 0:
    (x, y, z) = q.popleft()
    neighbours = get_neighbours(x, y, z)
    for neighbour in neighbours:
        if not is_in_bound(neighbour):
            continue
        if neighbour in droplet_set:
            outer_area += 1
        elif neighbour not in outer_air_set:
            outer_air_set.add(neighbour)
            q.append(neighbour)


print("res 1 =", total_area)
print("res 2 =", outer_area)

