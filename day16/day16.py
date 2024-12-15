from collections import deque
import re
"""
Valve WW has flow rate=0; tunnels lead to valves QH, YZ
Valve HB has flow rate=15; tunnel leads to valve OM
"""
lines = open("input.txt", "r").read().splitlines()
# lines = open("test_input.txt", "r").read().splitlines()

path_map = dict()
node_length_map = dict()

for line in lines:
    pattern = r"Valve (\w+) has flow rate=(\d+); \w+ \w+ to \w+ (\w+(:?, \w+)*)"
    match = re.match(pattern, line)
    assert match is not None
    source, rate, sinks, _ = match.groups()
    rate = int(rate)
    sinks = sinks.split(", ")
    path_map[source] = (rate, set(sinks))

def get_smallest_path_len(start_node, dest_node):
    seen_node = set([start_node])
    q = deque([(start_node, 0)])
    while q.__len__() > 0:
        (cur_node, curLen) = q.popleft()
        if cur_node == dest_node:
            return curLen
        seen_node.add(cur_node)
        (_, valve_paths) = path_map[cur_node]
        for path in valve_paths:
            if path not in seen_node:
                q.append((path, curLen + 1))
    raise Exception("Unreachable")

MINUTES = 30
MAX_RATE = 0
working_valves = set()

for (key,(rate, _)) in path_map.items():
    if rate != 0:
        working_valves.add(key)
        MAX_RATE += rate

key_nodes = list(working_valves) + ["AA"]
for (i, start_node) in enumerate(key_nodes):
    for dest_node in key_nodes[i+1:]:
        len = get_smallest_path_len(start_node, dest_node)
        node_length_map[(start_node, dest_node)] = len
        node_length_map[(dest_node, start_node)] = len

results1 = set([0])
max_leaks = dict()
q = deque([("AA", 0, 0, 0, frozenset())])

while q.__len__() > 0:
    (cur, cur_time, cur_rate, cur_leak, cur_opened) = q.popleft()
    if cur_time == MINUTES:
        results1.add(cur_leak)
        continue
    if cur_rate == MAX_RATE:
        results1.add(cur_leak + cur_rate * (MINUTES - cur_time))
        continue
    (valve_rate, _) = path_map[cur]
    new_destinations = working_valves - cur_opened
    for new_dest in new_destinations:
        len = get_smallest_path_len(cur, new_dest)
        (dest_rate, _) = path_map[new_dest]
        if MINUTES - (len + cur_time + 1) <= 0:
            results1.add(cur_leak + cur_rate * (MINUTES - cur_time))
            continue
        new_acc_rate = cur_rate + dest_rate
        new_leaked = cur_leak + cur_rate * (len + 1) 
        new_cost = cur_time + len + 1
        new_tuple = (new_dest, cur_time + len + 1, new_acc_rate, new_leaked, cur_opened | set([new_dest]))
        q.append(new_tuple)


res1 = max(results1)
print("res1 =", res1)

