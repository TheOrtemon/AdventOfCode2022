from collections.abc import Callable
from collections import deque
from dataclasses import dataclass
from operator import mul, add
from copy import deepcopy

test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


@dataclass
class Monkey:
    items: deque[int] | None
    operation: Callable[[int], int] | None
    test: Callable[[int], bool] | None
    if_true: int | None 
    if_false: int | None
    counter: int = 0


# lines = test_input.splitlines()
lines = open("input.txt", "r").read().splitlines()

monkeys: list[Monkey] = []
lcm = 1

for line in lines:
    if line.startswith("Monkey"):
        monkeys.append(Monkey(None, None, None, None, None))
    elif line.startswith("  Starting items: "):
        items_str = line[len("  Starting items: "):]
        items = deque([int(item) for item in items_str.split(", ")])
        monkeys[-1].items = items
    elif line.startswith("  Operation: new = "):
        equation = line[len("  Operation: new = "):]
        a, op, b = equation.split()
        def res_func(old: int, a=a, op=op, b=b) -> int:
            match op:
                case "*":
                    do = mul
                case _:
                    do = add
            arg1 = old if a == "old" else int(a)
            arg2 = old if b == "old" else int(b)
            return do(arg1, arg2)
        monkeys[-1].operation = res_func
    elif line.startswith("  Test: divisible by "):
        n = int(line[len("  Test: divisible by "):])
        lcm *= n
        def tester(x: int, n=n) -> bool:
            return x % n == 0
        monkeys[-1].test = tester
    elif line.startswith("    If true: throw to monkey "):
        n = int(line[len("    If true: throw to monkey "):])
        monkeys[-1].if_true = n
    elif line.startswith("    If false: throw to monkey "):
        n = int(line[len("    If false: throw to monkey "):])
        monkeys[-1].if_false = n
    elif line.isspace() or line == "":
        pass
    else:
        print(line.__repr__())
        raise Exception("Unreachable")

monkeys2 = deepcopy(monkeys)

for _ in range(20):
    for monkey in monkeys:
        assert monkey.items is not None
        assert monkey.operation is not None
        assert monkey.test is not None
        assert monkey.if_true is not None
        assert monkey.if_false is not None
        monkey.counter += len(monkey.items)
        while monkey.items:
            worry_level = monkey.items.popleft()
            new_worry_level = monkey.operation(worry_level) // 3
            if monkey.test(new_worry_level):
                monkey_num = monkey.if_true
            else:
                monkey_num = monkey.if_false
            next_monkey = monkeys[monkey_num]
            assert next_monkey.items is not None
            next_monkey.items.append(new_worry_level)

# print(monkeys)
counters = sorted(monkey.counter for monkey in monkeys)
res = counters[-1] * counters[-2]

print(res)

for i in range(10_000):
    for monkey in monkeys2:
        assert monkey.items is not None
        assert monkey.operation is not None
        assert monkey.test is not None
        assert monkey.if_true is not None
        assert monkey.if_false is not None
        monkey.counter += len(monkey.items)
        while monkey.items:
            worry_level = monkey.items.popleft()
            new_worry_level = monkey.operation(worry_level) % lcm
            if monkey.test(new_worry_level):
                monkey_num = monkey.if_true
            else:
                monkey_num = monkey.if_false
            next_monkey = monkeys2[monkey_num]
            assert next_monkey.items is not None
            next_monkey.items.append(new_worry_level)

counters2 = sorted(monkey.counter for monkey in monkeys2)
res2 = counters2[-1] * counters2[-2]

print(res2)
