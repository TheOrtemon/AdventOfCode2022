from ast import literal_eval
from collections.abc import Generator
from itertools import zip_longest
from functools import cmp_to_key
test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

# lines = test_input.splitlines()
lines = open("input.txt", "r").read().splitlines()

type NestedList = list[int | NestedList]

def parse_nested_list(nested_list: NestedList) -> Generator[int, None, None]:
    for item in nested_list:
        if isinstance(list, item):
            yield from parse_nested_list(item)
        else:
            yield item


def compare_lists(a: NestedList, b: NestedList) -> bool | None:
    for x, y in zip_longest(a, b):
        if x is None:
            return True
        elif y is None:
            return False
        elif isinstance(x, list) and isinstance(y, list):
            local_res = compare_lists(x, y)
            if isinstance(local_res, bool):
                return local_res
            continue
        elif isinstance(x, list):
            local_res = compare_lists(x, [y]) 
            if isinstance(local_res, bool):
                return local_res
        elif isinstance(y, list):
            local_res = compare_lists([x], y) 
            if isinstance(local_res, bool):
                return local_res
        elif x < y:
            return True
        elif x > y:
            return False

acc = 0
packet_list: list[NestedList] = []

for id, i in enumerate(range(0, len(lines), 3)):
    a_line, b_line = lines[i:i+2]
    a: NestedList = literal_eval(a_line)
    b: NestedList = literal_eval(b_line)
    packet_list += [a, b]

    local_res = compare_lists(a, b)
    if local_res:
        acc += id + 1

    # print(a_line, " and ", b_line, "returns ", local_res)

print("res 1 = ", acc)

divider_packets: list[NestedList] = [[[2]], [[6]]]
packet_list += divider_packets
packet_list.sort(key=cmp_to_key(lambda x, y: 1 if compare_lists(x,y) else -1), reverse=True)

res2 = [packet_list.index(divider) + 1 for divider in divider_packets]
print("res2 ", res2[0] * res2[1])
