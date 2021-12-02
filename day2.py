with open("day2.in") as f:
    lines = f.readlines()


pos = [0, 0]
for line in lines:
    dir, units = line.split()
    units = int(units)

    if dir == "forward":
        pos[0] += units
    elif dir == "backward":
        pos[0] -= units
    elif dir == "up":
        pos[1] -= units
    elif dir == "down":
        pos[1] += units

print(pos[0] * pos[1])


pos = [0, 0]
aim = 0
for line in lines:
    dir, units = line.split()
    units = int(units)

    if dir == "forward":
        pos[0] += units
        pos[1] += units * aim
    elif dir == "backward":
        pos[0] -= units
    elif dir == "up":
        aim -= units
    elif dir == "down":
        aim += units

print(pos[0] * pos[1])
