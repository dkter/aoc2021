from collections import Counter

def do_thing(string, rules):
    new_string = []
    for index in range(len(string) - 1):
        pair = string[index] + string[index + 1]
        new_string.append(string[index])
        if pair in rules:
            new_string.append(rules[pair])
        else:
            print(f"i don't think this should happen: {pair}")
    new_string.append(string[-1])
    return "".join(new_string)


rules = {}
with open("day14.in") as f:
    template = f.readline().strip()
    f.readline()
    for line in f:
        ab, c = line.strip().split(" -> ")
        rules[ab] = c


for i in range(10):
    template = do_thing(template, rules)

c = Counter(template)
freq = c.most_common()
print(freq[0][1] - freq[-1][1])


# for i in range(30):
#     print(10 + i)
#     template = do_thing(template, rules)

# c = Counter(template)
# freq = c.most_common()
# print(freq[0][1] - freq[-1][1])


# might be able to break this down like last time

# actually. literally just memoize it
# NN -> {N: 2} -> {N: 2, C: 1} -> {N: 2, C: 2, B: 2}
# this might not work because order matters

# i might just do what i did last time and do the thing for every pair until 20
# not exactly what i did last time, actually

after_20 = {}
for rule in rules:
    string = rule
    for i in range(20):
        string = do_thing(string, rules)

    c = Counter(string)
    after_20[rule] = c


# do up until 20 and then look at the dict for the rest

for i in range(10): # 10 has already been done
    template = do_thing(template, rules)


total_count = Counter()
for index in range(len(template) - 1):
    pair = template[index] + template[index + 1]
    total_count.update(after_20[pair])

# okay this is a bug
# need to subtract the inner elements because they're counted twice by
# the individual counters
to_subtract = template[1:-1]
total_count.subtract(to_subtract)

freq = total_count.most_common()
print(freq[0][1] - freq[-1][1])
