import re
# lines = open("test_input.txt", "r").read().splitlines()
lines = open("input.txt", "r").read().splitlines()

sensors = []
beacons = []
dists = []
sens_ranges = []

test_y = 10

pattern = r".*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)"
for line in lines:
    if match := re.match(pattern, line):
        [sx, sy, bx, by] = [int(n) for n in match.groups()]
        dist = abs(sx - bx) + abs(sy - by)
        print("sensor coords:", sx, sy, "dist ", dist)
        sensors.append((sx, sy))
        beacons.append((bx, by))
        dists.append(dist)
        sens_length = dist - abs(sy - test_y)
        if sens_length < 0:
            continue

        sens_range = (sx - sens_length, sx + sens_length)
        sens_ranges.append(sens_range)

        # print("sens_l ", sens_length, "sens range ", sens_range)
    else:
        print("ERROR WITH: ", repr(line))

sens_ranges.sort(key=lambda a: a[0])
# print(sens_ranges)
cur_start, cur_end = sens_ranges[0]
combined_ranges = []

for start, end in sens_ranges[1:]:
    if start - cur_end <= 1:
        combined_ranges.append((cur_start, cur_end))
        cur_start = start
    cur_end = max(cur_end, end)
combined_ranges.append((cur_start, cur_end))
# print(combined_ranges)

res1 = sum(r[1] - r[0] for r in combined_ranges)
print(res1)

y_max = 4_000_001
for y in range(y_max):
    sens_ranges = []
    for (i, (xs, ys)) in enumerate(sensors):
        sens_length = dists[i] - abs(ys - y)
        if sens_length < 0:
            continue
        sens_range = (xs - sens_length, xs + sens_length)
        sens_ranges.append(sens_range)
    sens_ranges.sort(key=lambda a: a[0])

    combined_ranges = []
    cur_start, cur_end = sens_ranges[0]

    for start, end in sens_ranges[1:]:
        if start - cur_end > 1:
            combined_ranges.append((cur_start, cur_end))
            cur_start = start
        cur_end = max(cur_end, end)
    combined_ranges.append((cur_start, cur_end))

    # if combined_ranges:
    #     print("y = ", y, combined_ranges, sens_ranges)

    for i in range(combined_ranges.__len__() - 1):
        [(lrs, lre), (rrs, rre)] = combined_ranges[i:i+2]
        # if lre >= 0 and lrs < y_max and lre < rrs:
            # print(y, "Eurika ", lrs, lre, rrs, rre)
        if rrs - lre == 2:
            x = (rrs + lre) // 2
            # print("Eurika ", x, y)
            print("res 2 = ", x * 4000000 + y)
            break


