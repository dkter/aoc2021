from collections import deque
from queue import PriorityQueue

map = []
with open("day15.in") as f:
    for line in f:
        map.append([int(ch) for ch in line.strip()])

w = len(map[0])
h = len(map)


def get_surrounding(pos):
    # left
    if pos[0] != 0:
        yield (pos[0] - 1, pos[1])
    # right
    if pos[0] != w - 1:
        yield (pos[0] + 1, pos[1])
    # top
    if pos[1] != 0:
        yield (pos[0], pos[1] - 1)
    # bottom
    if pos[1] != h - 1:
        yield (pos[0], pos[1] + 1)


costs = {(0, 0): 0}
queue = PriorityQueue()
queue.put((0, (0, 0)))
visited = set()

while not queue.empty():
    risk, pos = queue.get()
    visited.add(pos)
    for surrounding in get_surrounding(pos):
        if surrounding not in visited:
            new_total_risk = costs[pos] + map[surrounding[1]][surrounding[0]]
            if surrounding not in costs or costs[surrounding] > new_total_risk:
                queue.put((new_total_risk, surrounding))
                costs[surrounding] = new_total_risk

#print(costs)
print(costs[(h-1, w-1)])
# 617 is wrong. so is 616


# generate new map
def next_value(value):
    if value == 9:
        return 1
    else:
        return value + 1

new_map = []
for row in map:
    new_map.append(
        row
        + [next_value(val) for val in row]
        + [next_value(next_value(val)) for val in row]
        + [next_value(next_value(next_value(val))) for val in row]
        + [next_value(next_value(next_value(next_value(val)))) for val in row]
    )
top5 = new_map[:]
for row in top5:
    new_map.append([next_value(val) for val in row])
for row in top5:
    new_map.append([next_value(next_value(val)) for val in row])
for row in top5:
    new_map.append([next_value(next_value(next_value(val))) for val in row])
for row in top5:
    new_map.append([next_value(next_value(next_value(next_value(val)))) for val in row])


w *= 5
h *= 5

def get_surrounding(pos):
    # left
    if pos[0] != 0:
        yield (pos[0] - 1, pos[1])
    # right
    if pos[0] != w - 1:
        yield (pos[0] + 1, pos[1])
    # top
    if pos[1] != 0:
        yield (pos[0], pos[1] - 1)
    # bottom
    if pos[1] != h - 1:
        yield (pos[0], pos[1] + 1)

costs = {(0, 0): 0}
queue = PriorityQueue()
queue.put((0, (0, 0)))
visited = set()

while not queue.empty():
    risk, pos = queue.get()
    visited.add(pos)
    for surrounding in get_surrounding(pos):
        if surrounding not in visited:
            new_total_risk = costs[pos] + new_map[surrounding[1]][surrounding[0]]
            if surrounding not in costs or costs[surrounding] > new_total_risk:
                queue.put((new_total_risk, surrounding))
                costs[surrounding] = new_total_risk

print(costs[(h-1, w-1)])
