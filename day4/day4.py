test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
acc1 = 0
acc2 = 0
with open("input.txt") as i:
    for line in i.readlines():

    # for line in test_input.splitlines():
        f_range, l_range = line.split(",")
        a, b = f_range.split("-")
        c, d = l_range.split("-")
        a, b, c, d = int(a), int(b), int(c), int(d)
        # print(a, b, c, d, "line ", line.__repr__())

        cond1 = c <= a and d >= b
        cond2 = a <= c and b >= d

        if cond1 or cond2:
            acc1 += 1

        cond3 = c <= b and d >= b
        cond4 = c <= a and d >= a
        cond5 = a <= c and b >= c
        cond6 = a <= d and b >= d
        if cond3 or cond4 or cond5 or cond6:
            acc2 += 1

print(acc1)
print(acc2)
