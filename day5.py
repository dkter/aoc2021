from itertools import combinations


def line_overlaps(line1, line2):
    if line1[0][0] == line1[1][0]:
        # x coords are the same
        if line2[0][0] == line2[1][0] == line1[0][0]:
            # x coords are the same
            line1_y_sorted = sorted([line1[0][1], line1[1][1]])
            line2_y_sorted = sorted([line2[0][1], line2[1][1]])

            if line1_y_sorted[0] <= line2_y_sorted[0] <= line2_y_sorted[1] <= line1_y_sorted[1]:
                return line2_y_sorted[1] - line2_y_sorted[0] + 1
            if line2_y_sorted[0] <= line1_y_sorted[0] <= line1_y_sorted[1] <= line2_y_sorted[1]:
                return line1_y_sorted[1] - line1_y_sorted[0] + 1
            if line2_y_sorted[0] <= line1_y_sorted[0] <= line2_y_sorted[1] <= line1_y_sorted[1]:
                return line2_y_sorted[1] - line1_y_sorted[0] + 1
            if line1_y_sorted[0] <= line2_y_sorted[0] <= line1_y_sorted[1] <= line2_y_sorted[1]:
                return line1_y_sorted[1] - line2_y_sorted[0] + 1
        elif line2[0][1] == line2[1][1]:
            # y coords are the same
            if (
                (
                    line2[0][0] <= line1[0][0] <= line2[1][0]
                    or line2[1][0] <= line1[0][0] <= line2[0][0]
                ) and (
                    line1[0][1] <= line2[0][1] <= line1[1][1]
                    or line1[1][1] <= line2[0][1] <= line1[0][1]
                )
            ):
                return 1
    elif line1[0][1] == line1[1][1]:
        # y coords are the same
        if line2[0][1] == line2[1][1] == line1[0][1]:
            # y coords are the same
            line1_x_sorted = sorted([line1[0][0], line1[1][0]])
            line2_x_sorted = sorted([line2[0][0], line2[1][0]])

            if line1_x_sorted[0] <= line2_x_sorted[0] <= line2_x_sorted[1] <= line1_x_sorted[1]:
                return line2_x_sorted[1] - line2_x_sorted[0] + 1
            if line2_x_sorted[0] <= line1_x_sorted[0] <= line1_x_sorted[1] <= line2_x_sorted[1]:
                return line1_x_sorted[1] - line1_x_sorted[0] + 1
            if line2_x_sorted[0] <= line1_x_sorted[0] <= line2_x_sorted[1] <= line1_x_sorted[1]:
                return line2_x_sorted[1] - line1_x_sorted[0] + 1
            if line1_x_sorted[0] <= line2_x_sorted[0] <= line1_x_sorted[1] <= line2_x_sorted[1]:
                return line1_x_sorted[1] - line2_x_sorted[0] + 1
        elif line2[0][0] == line2[1][0]:
            # x coords are the same
            if (
                (
                    line2[0][1] <= line1[0][1] <= line2[1][1]
                    or line2[1][1] <= line1[0][1] <= line2[0][1]
                ) and (
                    line1[0][0] <= line2[0][0] <= line1[1][0]
                    or line1[1][0] <= line2[0][0] <= line1[0][0]
                )
            ):
                return 1
    return 0


lines  = []
with open("day5.in") as file:
    for line in file:
        coord1, coord2 = line.split(" -> ")
        coord1 = tuple(int(i) for i in coord1.split(","))
        coord2 = tuple(int(i) for i in coord2.split(","))
        lines.append((coord1, coord2))

# overlaps = 0
# for line1, line2 in combinations(lines, 2):
#     # if lines_overlap(line1, line2):
#     #     print(line1, line2)
#     #     overlaps += 1
#     if line_overlaps(line1, line2):
#         print(line1, line2, line_overlaps(line1, line2))
#     overlaps += line_overlaps(line1, line2)

# i am going to scrap this approach
# new approach which will run way slower but probably work better

def draw_line(line):
    if line[0][0] == line[1][0]:
        # x coords are the same
        min_y = min(line[0][1], line[1][1])
        max_y = max(line[0][1], line[1][1])
        for y in range(min_y, max_y + 1):
            yield (line[0][0], y)
    elif line[0][1] == line[1][1]:
        # y coords are the same
        min_x = min(line[0][0], line[1][0])
        max_x = max(line[0][0], line[1][0])
        for x in range(min_x, max_x + 1):
            yield (x, line[0][1])

points = set()
overlapping_points = set()
for line in lines:
    for point in draw_line(line):
        if point in points:
            overlapping_points.add(point)
        else:
            points.add(point)

print(len(overlapping_points))


# pt2

def draw_line_diagonal(line):
    if line[0][0] == line[1][0]:
        # x coords are the same
        min_y = min(line[0][1], line[1][1])
        max_y = max(line[0][1], line[1][1])
        for y in range(min_y, max_y + 1):
            yield (line[0][0], y)
    elif line[0][1] == line[1][1]:
        # y coords are the same
        min_x = min(line[0][0], line[1][0])
        max_x = max(line[0][0], line[1][0])
        for x in range(min_x, max_x + 1):
            yield (x, line[0][1])
    else:
        if line[0][0] < line[1][0]:
            xstep = 1
        else:
            xstep = -1
        if line[0][1] < line[1][1]:
            ystep = 1
        else:
            ystep = -1
        for x, y in zip(
            range(line[0][0], line[1][0] + xstep, xstep),
            range(line[0][1], line[1][1] + ystep, ystep)
        ):
                yield (x, y)


points = set()
overlapping_points = set()
for line in lines:
    for point in draw_line_diagonal(line):
        if point in points:
            overlapping_points.add(point)
        else:
            points.add(point)

print(len(overlapping_points))
