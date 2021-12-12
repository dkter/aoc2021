from collections import deque
from pprint import pprint

def is_small(cave):
    return all(ch in "abcdefghijklmnopqrstuvwxyz" for ch in cave)


def connections(cave, tunnels):
    for tunnel in tunnels:
        if cave in tunnel:
            yield [c for c in tunnel if c != cave][0]


caves = set()
tunnels = []
with open("day12.in") as f:
    for line in f:
        a, b = line.strip().split("-")
        caves.add(a)
        caves.add(b)
        tunnels.append((a, b))


paths = []
queue = deque()
queue.append(("start", ("start",), frozenset({"start"}))) # current cave, path, visited
while queue:
    current_cave, path, visited_small = queue.pop()
    if current_cave == "end":
        paths.append(path)
        continue
    for conn in connections(current_cave, tunnels):
        if not (is_small(conn) and conn in visited_small):
            if is_small(conn):
                new_visited_small = visited_small | frozenset({conn})
            else:
                new_visited_small = visited_small
            queue.append((conn, path + (conn,), new_visited_small))

print(len(paths))


paths = []
queue = deque()
queue.append((
    "start",
    ("start",),
    frozenset({"start"}),
    frozenset({"start"}),
)) # current cave, path, visited_once, visited_twice
while queue:
    current_cave, path, visited_once, visited_twice = queue.pop()
    if current_cave == "end":
        paths.append(path)
        continue
    for conn in connections(current_cave, tunnels):
        if not (is_small(conn) and (conn in visited_twice or (len(visited_twice) == 2 and conn in visited_once))):
            new_visited_once = visited_once
            new_visited_twice = visited_twice
            if is_small(conn):
                if conn in visited_once:
                    new_visited_twice = visited_twice | frozenset({conn})
                new_visited_once = visited_once | frozenset({conn})
            queue.append((conn, path + (conn,), new_visited_once, new_visited_twice))

print(len(paths))
