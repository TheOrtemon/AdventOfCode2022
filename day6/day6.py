test_input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
# line = test_input
f = open("input.txt", "r")

line = f.readline()

for i in range(len(line) - 3):
    window = line[i:i+4]
    window_set = set(window)
    n = len(window_set)

    # print(window, n)
    if n == 4:
        print("answer is: ", i + 4)
        break


for i in range(len(line) - 13):
    window = line[i:i+14]
    window_set = set(window)
    n = len(window_set)

    # print(window, n)
    if n == 14:
        print("second answer is: ", i + 14)
        break
