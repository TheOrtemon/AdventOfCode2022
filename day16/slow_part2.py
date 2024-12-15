from typing import Deque, NamedTuple, Set, Tuple
from collections import deque
from itertools import combinations
import re

lines = open("input.txt", "r").read().splitlines()
# lines = open("test_input.txt", "r").read().splitlines()

def get_smallest_path_len(start_node, dest_node):
    dp_res = node_length_map.get((start_node, dest_node))
    if dp_res is not None:
        return dp_res
    seen_node = set([start_node])
    q = deque([(start_node, 0)])
    while q.__len__() > 0:
        (cur_node, curLen) = q.popleft()
        if cur_node == dest_node:
            return curLen
        seen_node.add(cur_node)
        valve_paths = path_map[cur_node]
        for path in valve_paths:
            if path not in seen_node:
                q.append((path, curLen + 1))
    raise Exception("Unreachable")

def get_combinations(items: Set):
    if items.__len__() < 2:
        return iter([(None, None)]) if (items.__len__() == 0) else iter([(next(iter(items)), None)])
    else:
        return combinations(items, 2)

path_map = dict()
rate_map = dict()
node_length_map = dict()

for line in lines:
    pattern = r"Valve (\w+) has flow rate=(\d+); \w+ \w+ to \w+ (\w+(:?, \w+)*)"
    match = re.match(pattern, line)
    assert match is not None
    source, rate, sinks, _ = match.groups()
    rate = int(rate)
    sinks = sinks.split(", ")
    path_map[source] = set(sinks)
    rate_map[source] = rate

MAX_RATE = 0
working_valves = set()

for (key,rate) in rate_map.items():
    if rate != 0:
        working_valves.add(key)
        MAX_RATE += rate

key_nodes = list(working_valves) + ["AA"]
for (i, start_node) in enumerate(key_nodes):
    for dest_node in key_nodes[i+1:]:
        len = get_smallest_path_len(start_node, dest_node)
        node_length_map[(start_node, dest_node)] = len
        node_length_map[(dest_node, start_node)] = len

MINUTES2 = 13
START_DEST = "AA"

results2 = set()
max_leaks2 = dict()

class Dude(NamedTuple):
    dest: str
    arriv_time: int

class Duet(NamedTuple):
    dude1: Dude
    dude2: Dude

class Step(NamedTuple):
    duet: Duet
    time: int
    rate: int
    leak: int
    opened: frozenset[str]

start_state = Duet(Dude(START_DEST, 0), Dude(START_DEST, 0))
starting_step = Step(start_state, 0, 0, 0, frozenset([]))
q2: Deque[Step] = deque([(starting_step)])
skipped = 0
max_time = 0

def new_step_one_to_open(still_dude: Dude, closed_dude: Dude, cur_step: Step) -> Step:
    """Just opening one"""
    upd_still_dude = Dude(still_dude.dest, still_dude.arriv_time - 1)
    updated_duet = Duet(upd_still_dude, closed_dude)
    new_time = cur_step.time + 1
    new_rate = cur_step.rate + rate_map[closed_dude.dest]
    new_leak = cur_step.leak + cur_step.rate
    new_opened = cur_opened | frozenset([closed_dude.dest])
    return Step(updated_duet, new_time, new_rate, new_leak, new_opened)

def new_step_two_to_open(cur_step: Step) -> Step:
    """Just opening two"""
    (dude1, dude2) = cur_step.duet
    cur_duet = cur_step.duet
    new_time = cur_step.time + 1
    new_rate = cur_step.rate + rate_map[dude1.dest] + rate_map[dude2.dest]
    new_leak = cur_step.leak + cur_step.rate
    diff_opened = frozenset([dude1.dest, dude2.dest])
    new_opened = (cur_step.opened | diff_opened)
    return Step(cur_duet, new_time, new_rate, new_leak, new_opened)

def new_step_two_closed_two_old(arrived_dude1: Dude, arrived_dude2: Dude, cur_step: Step) -> Step:
    """Dual going"""
    delta_time = min(arrived_dude1.arriv_time, arrived_dude2.arriv_time)
    new_time = cur_step.time + delta_time
    new_leak = cur_step.leak + cur_step.rate * delta_time
    new_dude1 = Dude(arrived_dude1.dest, arrived_dude1.arriv_time - delta_time)
    new_dude2 = Dude(arrived_dude2.dest, arrived_dude2.arriv_time - delta_time)
    new_duet = Duet(new_dude1, new_dude2)
    updated_step = Step(new_duet, new_time, cur_step.rate, new_leak, cur_step.opened)
    if new_dude1.arriv_time == new_dude2.arriv_time:
        res = new_step_two_to_open(updated_step)
    else:
        closed_dude, still_dude = (new_dude1, new_dude2) if new_dude1.arriv_time == 0 else (new_dude2, new_dude1)
        res = new_step_one_to_open(still_dude, closed_dude, updated_step)
    return res

def new_step_two_closed_one_new(new_dest: str | None, arrived_dude: Dude, still_dude: Dude, cur_step: Step) -> Step:
    """Arrived is closed so im dual going"""
    new_dest = new_dest or START_DEST
    new_cost = get_smallest_path_len(arrived_dude.dest, new_dest) if new_dest != START_DEST else still_dude.arriv_time
    new_dude = Dude(new_dest, new_cost)
    return new_step_two_closed_two_old(new_dude, still_dude, cur_step)

def new_step_one_to_open_one_new(new_dest: str | None, opened_dude: Dude, closed_dude: Dude, cur_step: Step) -> Step:
    """Arrived both zero"""
    new_dest = new_dest or START_DEST
    new_cost = get_smallest_path_len(opened_dude.dest, new_dest)
    new_dude = Dude(new_dest, new_cost)
    return new_step_one_to_open(new_dude, closed_dude, cur_step)

def get_init_dude(dest: str) -> Dude:
    arriv_time = get_smallest_path_len(START_DEST, dest)
    return Dude(dest, arriv_time)

type OptDest = str | None

def get_cross_pairs(arrived_duet: Duet, new_dests: Tuple[OptDest, OptDest]) -> Tuple[Duet, Duet]:
    (arr1, arr2) = arrived_duet
    (dest1, dest2) = (dest or START_DEST for dest in new_dests)
    new_duet1 = Duet(Dude(dest1, get_smallest_path_len(arr1.dest, dest1)), Dude(dest2, get_smallest_path_len(arr2.dest, dest2)))
    new_duet2 = Duet(Dude(dest2, get_smallest_path_len(arr1.dest, dest2)), Dude(dest1, get_smallest_path_len(arr2.dest, dest1)))
    return (new_duet1, new_duet2)

while q2.__len__() > 0:
    cur_step = q2.popleft() 
    (cur_duet, cur_time, cur_rate, cur_leak, cur_opened) = cur_step
    (dude1, dude2) = cur_duet
    if cur_time == MINUTES2 or cur_rate == MAX_RATE:
        results2.add(cur_leak + cur_rate * (MINUTES2 - cur_time))
        continue

    new_destinations = working_valves - (cur_opened | frozenset([dude1.dest, dude2.dest]))
    new_destinations_combinations = get_combinations(new_destinations)
    new_destinations = new_destinations if new_destinations.__len__() > 0 else [None]
    match (dude1.arriv_time, dude2.arriv_time):
        case (0, 0):
            if dude1.dest not in cur_opened or dude2.dest not in cur_opened:
                if dude1.dest not in cur_opened and dude2.dest not in cur_opened: # two closed
                    assert dude1.dest == START_DEST
                    several_duets = [Duet(get_init_dude(pair[0]), get_init_dude(pair[1])) 
                                     for pair in new_destinations_combinations]
                    several_steps = [Step(duet, cur_time, cur_rate, cur_leak, cur_opened) 
                                     for duet in several_duets]
                else: # one close
                    opened_dude, closed_dude = (dude1, dude2) if dude1.dest in cur_opened else (dude2, dude1)
                    assert rate_map.get(closed_dude.dest, 0) > 0
                    several_steps = [new_step_one_to_open_one_new(new_dest, opened_dude, closed_dude, cur_step) 
                                     for new_dest in new_destinations]
            else: 
                several_duets_nested = [get_cross_pairs(cur_duet, pair) for pair in new_destinations_combinations]
                several_duets = list(sum(several_duets_nested, ()))
                several_steps = [new_step_two_closed_two_old(duet.dude1, duet.dude2, cur_step) for duet in several_duets]
        case (0, _) | (_, 0):
            arrived_dude, still_dude = (dude1, dude2) if dude1.arriv_time == 0 else (dude2, dude1)
            if arrived_dude.dest not in cur_opened: # weird one
                assert arrived_dude.dest != START_DEST
                several_steps = [new_step_one_to_open(still_dude, arrived_dude, cur_step)]
            else:
                # print("normal one")
                several_steps = [new_step_two_closed_one_new(new_dest, arrived_dude, still_dude, cur_step) 
                                 for new_dest in new_destinations]
        case _:
            assert cur_step.opened.__len__() == 0
            new_step = new_step_two_closed_two_old(dude1, dude2, cur_step)
            several_steps = [new_step]

    res_steps = []
    for pot_step in several_steps:
        if MINUTES2 - pot_step.time < 0:
            results2.add(cur_leak + cur_rate * (MINUTES2 - cur_time))
            continue
        else:
            res_steps.append(pot_step)
    q2.extend(res_steps)

print(max(results2))
print("skipped", skipped)
