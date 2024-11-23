with open("input.txt") as i:
    acc = 0
    for line in i.readlines():
        a, b = line.split()
        res: int
        match b:
            case "X":
                points = 0
                match a:
                    case "A":
                        res = points + 3
                    case "B":
                        res = points + 1
                    case _:
                        res = points + 2
            case "Y":
                points = 3
                match a:
                    case "A":
                        res = points + 1
                    case "B":
                        res = points + 2
                    case _:
                        res = points + 3
            case _: # case Z
                points = 6
                match a:
                    case "A":
                        res = points + 2
                    case "B":
                        res = points + 3
                    case _:
                        res = points + 1
        acc += res


print(acc)
