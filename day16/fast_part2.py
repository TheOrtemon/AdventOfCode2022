from collections import deque, namedtuple
from dataclasses import dataclass
import re
from typing import Dict, FrozenSet, NamedTuple
from itertools import combinations

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

MAX_RATE = 0
MINUTES = 30
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

# print(node_length_map)

achivs: Dict[FrozenSet[str], int] = dict()
results1 = set([0])
max_leaks = dict()
q = deque([("AA", 0, 0, 0, frozenset())])

while q.__len__() > 0:
    (cur, cur_time, cur_rate, cur_leak, cur_opened) = q.popleft()
    if cur_time == MINUTES or cur_rate == MAX_RATE:
        # results1.add(cur_leak)
        achivs[cur_opened] = max(achivs.get(cur_opened, 0), cur_leak + cur_rate * (MINUTES - cur_time))
        continue
    (valve_rate, _) = path_map[cur]
    new_destinations = working_valves - cur_opened
    for new_dest in new_destinations:
        len = get_smallest_path_len(cur, new_dest)
        (dest_rate, _) = path_map[new_dest]
        if MINUTES - (len + cur_time + 1) <= 0:
            achivs[cur_opened] = max(achivs.get(cur_opened, 0), cur_leak + cur_rate * (MINUTES - cur_time))
            results1.add(cur_leak + cur_rate * (MINUTES - cur_time))
            continue
        new_acc_rate = cur_rate + dest_rate
        new_leaked = cur_leak + cur_rate * (len + 1) 
        new_cost = cur_time + len + 1
        new_tuple = (new_dest, cur_time + len + 1, new_acc_rate, new_leaked, cur_opened | set([new_dest]))
        q.append(new_tuple)

print(achivs.__len__())
res2 = 0
print("got achivs")
for (a, b) in combinations(achivs, 2):
    if (a.intersection(b)).__len__() == 0:
        res2 = max(res2, achivs[a] + achivs[b])


print("res2 =", res2)


# MINUTES2 = 26

# results2 = set([0])
# max_leaks2 = dict()

# class Duet(NamedTuple):
#     dest1: str
#     arriv_time1: int
#     dest2: str
#     arriv_time2: int

# class Step(NamedTuple):
#     duet: Duet
#     time: int
#     rate: int
#     leak: int
#     opened: frozenset[str]

# start_state = Duet("AA", 0, "AA", 0)
# starting_step = (start_state, 0, 0, 0, frozenset())
# q2 = deque([(starting_step)])
# skipped = 0



# print("skipped2 =", skipped)
# res2 = max(results2)
# print("res2 =", res2)
