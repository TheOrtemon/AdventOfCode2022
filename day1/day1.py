with open("input.txt") as i:
    acc = 0
    elves = []
    for line in i.readlines():
        if line == "\n":
            elves.append(acc)
            acc = 0
            continue
        acc += int(line)

elves.sort()
res1 = max(elves)
last3 = elves[-3:]
res2 = sum(last3)

print("first task: ", res1)
print("second task: ", res2)
