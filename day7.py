from statistics import median

with open("day7.in") as f:
    positions = [int(i) for i in f.readline().split(",")]


med = median(positions)
total_fuel = 0
for pos in positions:
    total_fuel += abs(pos - med)

print(total_fuel)


# pt2

def calculate_fuel(start, end):
    chg = 1
    fuel = 0
    if start > end:
        step = -1
    else:
        step = 1
    for i in range(start, end, step):
        fuel += chg
        chg += 1
    return fuel

def calculate_fuel(start, end):
    diff = abs(end - start)
    return diff * (diff + 1) // 2

# naive solution
min_fuel = None
for pos1 in range(min(positions), max(positions)):
    total_fuel = 0
    for pos2 in positions:
        total_fuel += calculate_fuel(pos1, pos2)
    if min_fuel is None or total_fuel < min_fuel:
        min_fuel = total_fuel

print(min_fuel)

# oh that worked
