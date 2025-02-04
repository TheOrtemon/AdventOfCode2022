input = open("input.txt", "r").read().strip()
# input = open("test_input.txt", "r").read().strip()

def snafu_to_dec(line):
    res = 0
    for i, c in enumerate(line[::-1]):
        match c:
            case "0":
                snafu_digit = 0
            case "1":
                snafu_digit = 1
            case "2":
                snafu_digit = 2
            case "-":
                snafu_digit = -1
            case "=":
                snafu_digit = -2
            case _:
                raise Exception("Unreachable")
        res += snafu_digit * (5 ** i)
    return res

def decdig_to_snafu(d):
    match d:
        case -2:
            return "="
        case -1:
            return "-"
        case 0:
            return "0"
        case 1:
            return "1"
        case 2:
            return "2"
        case _:
            raise Exception("Unreachable")

def dec_to_snafu(n):
    int_res = []
    borrow = 0
    while True:
        rem = n % 5
        rem += borrow
        n //= 5
        if rem >= 3:
            rem -= 5
            int_res.append(rem)
            borrow = 1
        else:
            int_res.append(rem)
            borrow = 0
        if n == 0:
            break
    snafu_res = [decdig_to_snafu(i) for i in int_res]

    return "".join(snafu_res[::-1])

res1 = 0
for line in input.splitlines():
    res1 += snafu_to_dec(line)

print("res1=", dec_to_snafu(res1))
