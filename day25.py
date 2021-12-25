from itertools import count
from pprint import pprint

def step(map):
    h = len(map)
    w = len(map[0])
    new_map = [["." for x in range(w)] for y in range(h)]
    nmoves = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == ">":
                if x == w - 1 and map[y][0] == ".":
                    new_map[y][0] = ">"
                    nmoves += 1
                elif x != w - 1 and map[y][x + 1] == ".":
                    new_map[y][x + 1] = ">"
                    nmoves += 1
                else:
                    new_map[y][x] = ">"
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "v":
                if y == h - 1 and new_map[0][x] == "." and map[0][x] != "v":
                    new_map[0][x] = "v"
                    nmoves += 1
                    continue
                elif y != h - 1 and new_map[y + 1][x] == "." and map[y + 1][x] != "v":
                    new_map[y + 1][x] = "v"
                    nmoves += 1
                    continue
                else:
                    new_map[y][x] = "v"
    return new_map, nmoves


def mapprint(map):
    for row in map:
        for cell in row:
            print(cell, end="")
        print("")


map = []
with open("day25.in") as f:
    for line in f:
        map.append(list(line.strip()))


new_map = map
for i in count(1):
    new_map, nmoves = step(new_map)
    if nmoves == 0:
        print(i)
        break

