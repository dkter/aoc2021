with open("day6.in") as f:
    lanternfish = [int(i) for i in f.readline().split(",")]
lanternfish_pt2 = lanternfish[:]


lanternfish = [6]
fish_dict = {}
for i in range(81):
    new_lanternfish = []
    for fish in lanternfish:
        if fish == 0:
            new_lanternfish.append(6)
            new_lanternfish.append(8)
        else:
            new_lanternfish.append(fish - 1)
    lanternfish = new_lanternfish
    if i >= 80-6:
        fish_dict[i] = len(lanternfish)
print(fish_dict)
lanternfish = [0]
fish_dict = {}
for i in range(82):
    new_lanternfish = []
    for fish in lanternfish:
        if fish == 0:
            new_lanternfish.append(6)
            new_lanternfish.append(8)
        else:
            new_lanternfish.append(fish - 1)
    lanternfish = new_lanternfish
    if i >= 80-6:
        fish_dict[i] = len(lanternfish)

print(fish_dict)

total_fish = 0
for fish in lanternfish_pt2:
    total_fish += fish_dict[79 - fish]

print(total_fish)
