with open("day6.in") as f:
    lanternfish = [int(i) for i in f.readline().split(",")]
lanternfish_pt2 = lanternfish[:]

for i in range(80):
    new_lanternfish = []
    for fish in lanternfish:
        if fish == 0:
            new_lanternfish.append(6)
            new_lanternfish.append(8)
        else:
            new_lanternfish.append(fish - 1)
    lanternfish = new_lanternfish


print(len(lanternfish))

# part 2

def lanternfish_after_memo(initial_fish, days, memo):
    total_fish = 0
    for fish in initial_fish:
        total_fish += memo[days - 1 - fish]
    return total_fish

def lanternfish_after(initial_fish, days):
    # this is only gonna work for even days bc im lazy
    lanternfish = [0]
    fish_dict = {}
    for i in range(days // 2 + 1):
        new_lanternfish = []
        for fish in lanternfish:
            if fish == 0:
                new_lanternfish.append(6)
                new_lanternfish.append(8)
            else:
                new_lanternfish.append(fish - 1)
        lanternfish = new_lanternfish
        fish_dict[i] = len(lanternfish)

    fish_dict2 = {
        days - day: lanternfish_after_memo(lanternfish, days // 2 - day, fish_dict)
        for day in range(8)
    }

    return lanternfish_after_memo(initial_fish, days, fish_dict2)

print(lanternfish_after(lanternfish_pt2, 256))
