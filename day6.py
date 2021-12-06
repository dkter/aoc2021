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
# start with 0
# after 1 day, it results in 1 fish
# after 7 days, it results in 1 more fish / 2 fish
# after 9 days, it results in 1 more fish / 3 fish
# after 13 days, it results in 1 more fish / 4 fish
# ...
# just calculate what 1 fish does after 256 days, multiply by number of
# fish, and get the number of days right


lanternfish = [0]
fish_dict = {}
# for i in range(256):
#     print(i)
#     new_lanternfish = []
#     for fish in lanternfish:
#         if fish == 0:
#             new_lanternfish.append(6)
#             new_lanternfish.append(8)
#         else:
#             new_lanternfish.append(fish - 1)
#     lanternfish = new_lanternfish
#     if i >= 250:
#         fish_dict[i] = len(lanternfish)

# data_structure = []  # idk what to call this
# while (not data_structure) or all(i >= 256 for i in data_structure):


# print(fish_dict)

# total_fish = 0
# for fish in lanternfish_pt2:
#     total_fish += fish_dict[255 - fish]

# actually, this approach works, so i can just use it to break down the problem

def lanternfish_after(initial_fish, days, memo):
    total_fish = 0
    for fish in initial_fish:
        total_fish += memo[days - 1 - fish]
    return total_fish

# calculate lanternfish after only 128 days or something

lanternfish = [0]
fish_dict = {}
for i in range(128):
    new_lanternfish = []
    for fish in lanternfish:
        if fish == 0:
            new_lanternfish.append(6)
            new_lanternfish.append(8)
        else:
            new_lanternfish.append(fish - 1)
    lanternfish = new_lanternfish
    fish_dict[i] = len(lanternfish)

#print(fish_dict)

# we know what everything looks like after 128 days
# so, we can see what happens after 128 more days, for all 94508 items
# (this may not actually be that much faster)
# oh wait it will, because it's just a dict lookup

#print(lanternfish_after(lanternfish, 128, fish_dict))
# 6703087164 is wrong. but this runs instantly which is nice
# wait, i'm dumb
# i need to generate a new dict
fish_dict2 = {
    40 + i: lanternfish_after([0], i, fish_dict)
    for i in range(30, 41)
}

#print(fish_dict2)

#print(lanternfish_after(lanternfish_pt2, 80, fish_dict2))
# 1454793978760 also wrong
# try 80

# another implementation of part 1:
#print(lanternfish_after(lanternfish_pt2, 80, fish_dict))

# this works
# and "lanternfish" is the state of things after 128
# we want to see it after 128 more

# i am just going to write the code but better down here

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
