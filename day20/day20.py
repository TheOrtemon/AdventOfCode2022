input = open("input.txt", "r").read().strip().splitlines()
# input = open("test_input.txt", "r").read().strip().splitlines()

class Number:
    def __init__(self, index, num):
        self.index = index
        self.value = num


def solve(is_part2 = False):
    koef = 811589153 if is_part2 else 1
    times_koef = 10 if is_part2 else 1
    res_list = [int(line) * koef for line in input]
    order_list = [Number(i, int(line) * koef) for i, line in enumerate(input)]
    SIZE = len(order_list) - 1
    for i in range(len(order_list) * times_koef):
        i %= len(order_list)
        cur_num = order_list[i]
        mod = cur_num.value % SIZE
        if mod == 0:
            continue
        starting_index = cur_num.index
        res_list.pop(starting_index)
        res_index = (starting_index + mod) % SIZE
        if res_index == 0 and cur_num.value < 0:
            res_index = SIZE
        for num in order_list:
            if num is cur_num:
                num.index = res_index
            elif res_index <= num.index < starting_index:
                num.index += 1
            elif res_index >= num.index > starting_index:
                num.index -= 1

        res_list = [*res_list[:res_index], cur_num.value, *res_list[res_index:]]
    starting_index = res_list.index(0)
    a, b, c = (
            res_list[(starting_index + 1000) % (SIZE + 1)], 
            res_list[(starting_index + 2000) % (SIZE + 1)], 
            res_list[(starting_index + 3000) % (SIZE + 1)]
            )
    return a + b + c


print("res1 =", solve())
print("res2 =", solve(True))


