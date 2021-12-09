from collections import namedtuple, deque

Point = namedtuple("Point", ["x", "y"])

def is_low_point(map, xpos, ypos, cell):
    left_higher = (
        xpos == 0
        or map[ypos][xpos - 1] > cell
    )
    right_higher = (
        xpos == len(map[0]) - 1
        or map[ypos][xpos + 1] > cell
    )
    top_higher = (
        ypos == 0
        or map[ypos - 1][xpos] > cell
    )
    bottom_higher = (
        ypos == len(map) - 1
        or map[ypos + 1][xpos] > cell
    )
    return left_higher and right_higher and top_higher and bottom_higher

map = []
with open("day9.in") as f:
    for line in f:
        map.append([int(i) for i in line.strip()])

total = 0
low_points = []
for ypos, row in enumerate(map):
    for xpos, cell in enumerate(row):
        if is_low_point(map, xpos, ypos, cell):
            total += cell + 1
            low_points.append(Point(xpos, ypos))

print(total)

# pt2

def basin_size(map, point):
    size = 1
    visited = {point}  # i don't think it's possible to have a cycle here but just in case
    queue = deque([point])
    while queue:
        point = queue.pop()
        cell = map[point.y][point.x]
        to_add = []
        # left
        if (
            point.x != 0
            and map[point.y][point.x - 1] > cell
            and map[point.y][point.x - 1] != 9
            and Point(point.x - 1, point.y) not in visited
        ):
            to_add.append(Point(point.x - 1, point.y))
        # right
        if (
            point.x != len(map[0]) - 1
            and map[point.y][point.x + 1] > cell
            and map[point.y][point.x + 1] != 9
            and Point(point.x + 1, point.y) not in visited
        ):
            to_add.append(Point(point.x + 1, point.y))
        # top
        if (
            point.y != 0
            and map[point.y - 1][point.x] > cell
            and map[point.y - 1][point.x] != 9
            and Point(point.x, point.y - 1) not in visited
        ):
            to_add.append(Point(point.x, point.y - 1))
        # bottom
        if (
            point.y != len(map) - 1
            and map[point.y + 1][point.x] > cell
            and map[point.y + 1][point.x] != 9
            and Point(point.x, point.y + 1) not in visited
        ):
            to_add.append(Point(point.x, point.y + 1))
        queue.extend(to_add)
        size += len(to_add)
        visited.update(to_add)


    return size


basins = []
for point in low_points:
    basins.append(basin_size(map, point))

basins.sort()
product = basins[-1] * basins[-2] * basins[-3]

print(product)
