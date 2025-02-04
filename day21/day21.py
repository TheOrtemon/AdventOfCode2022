from functools import cache

input = open("input.txt", "r").read().strip().splitlines()
# input = open("test_input.txt", "r").read().strip().splitlines()

graph = {}

def get_evaluator(arg1, op, arg2):
    def evaluate(arg):
        graph_value = graph[arg]
        if isinstance(graph_value, int):
            return graph_value
        else:
            return graph_value()

    def evaluator(arg1=arg1, op=op, arg2=arg2):
        arg1_value = evaluate(arg1)
        arg2_value = evaluate(arg2)
        match op:
            case "+":
                return arg1_value + arg2_value
            case "-":
                return arg1_value - arg2_value
            case "*":
                return arg1_value * arg2_value
            case "/":
                return arg1_value / arg2_value
            case _:
                raise Exception("Unreachable")

    return evaluator
            

for line in input:
    node, expr = line.split(": ")
    if expr.isnumeric():
        graph[node] = int(expr)
    else:
        arg1, op, arg2 = expr.split(" ")
        graph[node] = get_evaluator(arg1, op, arg2)
        if node == "root":
            root_arg1 = arg1
            root_arg2 = arg2

@cache
def get_diff(humn):
    graph["humn"] = humn
    root_arg1_value = graph[root_arg1]()
    root_arg2_value = graph[root_arg2]()
    return abs(root_arg1_value - root_arg2_value)

def solve_part2():
    prev_diff = None
    lower, upper = None, None
    humn = 1
    while True:
        diff = get_diff(humn)
        if prev_diff is not None:
            diff_growth = diff - prev_diff
            if diff_growth > 0:
                upper = humn
                lower = humn // 4
                break
        humn *= 2
        prev_diff = diff

    while upper - lower > 1:
        mid = (lower + upper) // 2
        left_diff = get_diff(mid - 1)
        right_diff = get_diff(mid + 1)

        if right_diff < left_diff:
            lower = mid
        else:
            upper = mid

    if get_diff(upper) <= get_diff(lower):
        return upper
    else:
        return lower

res1 = int(graph["root"]())
res2 = solve_part2()

print("res1 =", res1)
print("res2 =", res2)

