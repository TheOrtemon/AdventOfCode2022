test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

f = open("input.txt", "r")
lines = f.readlines()

# lines = test_input.splitlines()

type File = int
type Dir = dict[str, File | Dir]

root: Dir = {"/": {}}
cur_dir_path: list[str] = []
cur_dir = root

line_num = 0

while line_num < lines.__len__():
    line = lines[line_num].strip()
    if line.startswith("$ cd .."):
        cur_dir_path.pop()
        cur_dir = root
        for dir in cur_dir_path:
            cur_dir = cur_dir[dir]
    elif line.startswith("$ cd "):
        dir_name = line[5:]
        cur_dir_path.append(dir_name)
        cur_dir = cur_dir[dir_name]
    elif line.startswith("dir "):
        dir_name = line[4:]
        cur_dir[dir_name] = {}
    elif line.startswith("$ ls"):
        pass
    elif line[0].isdigit():
        size, name = line.split(" ")
        cur_dir[name] = int(size)
    else:
        raise Exception("Unreachable")

    line_num += 1

litl_dir_size = {"value": 0}
dir_sizes = []

def calc_dir_weight(dir: Dir) -> int:
    res = 0
    for v in dir.values():
        if isinstance(v, dict):
            v = calc_dir_weight(v)
            dir_sizes.append(v)
            if v <= 100_000:
                litl_dir_size["value"] += v
        res += v
    return res




total_size = calc_dir_weight(root) 
dir_sizes.sort()
print(litl_dir_size)

for size in dir_sizes:
    sum_size = total_size - size
    if sum_size <= 40_000_000:
        print("second res: ", size)
        break



