import re
from functools import cache

input = open("input.txt", "r").read().strip().splitlines()
# input = open("test_input.txt", "r").read().strip().splitlines()

"""Blueprint 1:
Each ore robot costs 4 ore. 
Each clay robot costs 2 ore. 
Each obsidian robot costs 3 ore and 14 clay. 
Each geode robot costs 2 ore and 7 obsidian."""

TIME = 24

class MiningState:
    def __init__(self, time, ore, clay, obsidian, geode, 
                 ore_robot, clay_robot, obsidian_robot, geode_robot):
        self.time = time
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geode_robot = geode_robot

    def __hash__(self):
        return hash((
            self.time, self.ore, self.clay, self.obsidian, 
            self.geode, self.ore_robot, self.clay_robot, 
            self.obsidian_robot, self.geode_robot
        ))

    def __eq__(self, other):
        if isinstance(other, MiningState):
            return (
                self.time == other.time and
                self.ore == other.ore and
                self.clay == other.clay and
                self.obsidian == other.obsidian and
                self.geode == other.geode and
                self.ore_robot == other.ore_robot and
                self.clay_robot == other.clay_robot and
                self.obsidian_robot == other.obsidian_robot and
                self.geode_robot == other.geode_robot
            )
        return False

    def copy(self):
        return MiningState(
            self.time, self.ore, self.clay, self.obsidian, 
            self.geode, self.ore_robot, self.clay_robot, 
            self.obsidian_robot, self.geode_robot
        )

    def with_field(self, **kwargs):
        new_instance = self.copy()
        for key, value in kwargs.items():
            if hasattr(new_instance, key):
                setattr(new_instance, key, value)
        return new_instance

@cache
def find_best_state(cur_state: MiningState, min_left: int, inted_blueprint) -> int:
    if min_left == 1:
        return cur_state.geode + cur_state.geode_robot
    results = []
    _, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost = inted_blueprint
    max_ore = max(ore_cost, clay_cost, obs_ore_cost, geode_ore_cost)
    max_ore_cost = max(ore_cost, clay_cost, obs_ore_cost, geode_ore_cost)
    new_state_template = cur_state.with_field(
            time=cur_state.time + 1, 
            ore=cur_state.ore + cur_state.ore_robot,
            clay=cur_state.clay + cur_state.clay_robot,
            obsidian=cur_state.obsidian + cur_state.obsidian_robot,
            geode=cur_state.geode + cur_state.geode_robot)
    if cur_state.obsidian >= geode_obs_cost and cur_state.ore >= geode_ore_cost:
        new_state = new_state_template.with_field(
                obsidian=new_state_template.obsidian - geode_obs_cost, 
                ore=new_state_template.ore - geode_ore_cost,
                geode_robot=new_state_template.geode_robot + 1)
        results.append(new_state)
    if cur_state.clay >= obs_clay_cost and cur_state.ore >= obs_ore_cost and cur_state.obsidian_robot < geode_obs_cost:
        new_state = new_state_template.with_field(
                clay=new_state_template.clay - obs_clay_cost, 
                ore=new_state_template.ore - obs_ore_cost,
                obsidian_robot=new_state_template.obsidian_robot + 1)
        results.append(new_state)
    if cur_state.ore >= clay_cost and cur_state.clay_robot < obs_clay_cost:
        new_state = new_state_template.with_field(
                ore=new_state_template.ore - clay_cost,
                clay_robot=new_state_template.clay_robot + 1)
        results.append(new_state)
    if cur_state.ore >= ore_cost and cur_state.ore_robot < max_ore_cost:
        new_state = new_state_template.with_field(
                ore=new_state_template.ore - ore_cost,
                ore_robot=new_state_template.ore_robot + 1)
        results.append(new_state)
    if (cur_state.ore_robot < max_ore_cost and 
        cur_state.ore <= max_ore and
        (geode_obs_cost > cur_state.obsidian)) or len(results) == 0:
        results.append(new_state_template)
    return max(find_best_state(res, min_left - 1, inted_blueprint) for res in results)


def process_blueprint(blueprint, is_part2 = False):
    pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\."
    res = re.findall(pattern, blueprint)
    inted_blueprint = tuple(int(n) for n in res[0])
    init_state = MiningState(0, 0, 0, 0, 0, 1, 0, 0, 0)
    local_time = 32 if is_part2 else TIME
    res = find_best_state(init_state, local_time, inted_blueprint)
    if is_part2:
        return res
    return inted_blueprint[0] * res

res1 = 0
res2 = 1

for blueprint in input:
    res1 += process_blueprint(blueprint)
print("res1 =", res1)
for blueprint in input[:3]:
    res2 *= process_blueprint(blueprint, is_part2 = True)

print("res2 =", res2)
