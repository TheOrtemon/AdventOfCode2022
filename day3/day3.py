acc = 0
acc2 = 0
q = []
with open("input.txt") as i:
    for line in i.readlines():
        n = len(line)//2
        f_half = line[:n]
        s_half = line[n:]
        f_set, s_set = set(f_half), set(s_half)
        inter = f_set & s_set
        c = inter.__iter__().__next__()
        o = ord(c)
        n = o - 96 if o > 96 else o - 38
        acc += n

        q.append(set(line[:-1]))
        if len(q) % 3 != 0:
            continue
        inter2 = q[-1] & q[-2] & q[-3]
        # print("inter2 = ", inter2, repr(line))
        c2 = next(iter(q[-1] & q[-2] & q[-3]))
        o2 = ord(c2)
        n2 = o2 - 96 if o2 > 96 else o2 - 38
        acc2 += n2


print(acc)
print(acc2)
        
