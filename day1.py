with open("day1.in") as f:
    lines = f.readlines()
    int_lines = [int(line) for line in lines]

prev_line = 9999999999999
count = 0
for line in int_lines:
    if line > prev_line:
        count += 1
    prev_line = line

print(count)


prev_sum = 99999999999999999999
count = 0
for index in range(len(int_lines) - 2):
    sum = int_lines[index] + int_lines[index + 1] + int_lines[index + 2]
    if sum > prev_sum:
        count += 1
    prev_sum = sum

print(count)
