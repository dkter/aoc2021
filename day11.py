from itertools import count

w = 10
h = 10

def get_surrounding(pos):
    # left
    if pos[0] != 0:
        yield (pos[0] - 1, pos[1])
        # top left
        if pos[1] != 0:
            yield (pos[0] - 1, pos[1] - 1)
        # bottom left
        if pos[1] != h - 1:
            yield (pos[0] - 1, pos[1] + 1)
    # right
    if pos[0] != w - 1:
        yield (pos[0] + 1, pos[1])
        # top right
        if pos[1] != 0:
            yield (pos[0] + 1, pos[1] - 1)
        # bottom right
        if pos[1] != h - 1:
            yield (pos[0] + 1, pos[1] + 1)
    # top
    if pos[1] != 0:
        yield (pos[0], pos[1] - 1)
    # bottom
    if pos[1] != h - 1:
        yield (pos[0], pos[1] + 1)


def get_greater_than_nine(octopuses):
    for ypos, row in enumerate(octopuses):
        for xpos, cell in enumerate(row):
            if cell > 9:
                yield (xpos, ypos)


def step(octopuses):
    new_octopuses = []
    for row in octopuses:
        new_octopuses.append([e + 1 for e in row])

    flashed = set()
    done = False
    while not done:
        done = True
        for pos in get_greater_than_nine(new_octopuses):
            if pos not in flashed:
                done = False
                flashed.add(pos)
                for pos2 in get_surrounding(pos):
                    new_octopuses[pos2[1]][pos2[0]] += 1

    for pos in flashed:
        new_octopuses[pos[1]][pos[0]] = 0

    return len(flashed), new_octopuses


octopuses = []
with open("day11.in") as f:
    for line in f:
        octopuses.append([int(c) for c in line.strip()])

pt1_octopuses = octopuses[:]
total_flashes = 0
for i in range(100):
    flashes, pt1_octopuses = step(pt1_octopuses)
    total_flashes += flashes

print(total_flashes)

# part 2

for i in count(1):
    flashes, octopuses = step(octopuses)
    if flashes == 100:
        print(i)
        break
