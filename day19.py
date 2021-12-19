from itertools import permutations, combinations
from pprint import pprint
from collections import Counter


def rotations(positions):
    # for xsign in (1, -1):
    #     for ysign in (1, -1):
    #         for zsign in (1, -1):
    #             yield from [
    #                 [
    #                     (pos[ic[0]] * xsign, pos[ic[1]] * ysign, pos[ic[2]] * zsign)
    #                     for pos in positions
    #                 ]
    #                 for ic in permutations((0, 1, 2))
    #             ]
    # for ic in permutations((0, 1, 2)):
    #     for rotation in (
    #         (1, 1, 1),
    #         (-1, -1, -1),
    #         ()
    #     ):
    #         pass
    # yield positions
    # yield [
    #     -y, x, z
    #     for x, y, z in positions
    # ]
    # yield [
    #     -x, -y, z
    #     for x, y, z in positions
    # ]
    # yield [
    #     y, -x, z
    #     for x, y, z in positions
    # ]

    # yield [
    #     -z, y, x
    #     for x, y, z in positions
    # ]

    for facing_axis in (0, 1, 2):
        for facing_dir in (1, -1):
            if facing_axis == 0:
                axis0 = 2
                axis1 = 1
                dir0 = -1
                dir1 = 1
            elif facing_axis == 1:
                axis0 = 2
                axis1 = 0
                dir0 = -1
                dir1 = -1
            elif facing_axis == 2:
                axis0 = 0
                axis1 = 1
                dir0 = 1
                dir1 = 1

            yield [
                (
                    pos[axis0] * dir0 * facing_dir,
                    pos[axis1] * dir1,
                    pos[facing_axis] * facing_dir,
                )
                for pos in positions
            ]
            yield [
                (
                    pos[axis1] * dir1 * facing_dir * -1,
                    pos[axis0] * dir0,
                    pos[facing_axis] * facing_dir,
                )
                for pos in positions
            ]
            yield [
                (
                    pos[axis0] * dir0 * facing_dir * -1,
                    pos[axis1] * dir1 * -1,
                    pos[facing_axis] * facing_dir,
                )
                for pos in positions
            ]
            yield [
                (
                    pos[axis1] * dir1 * facing_dir,
                    pos[axis0] * dir0 * -1,
                    pos[facing_axis] * facing_dir,
                )
                for pos in positions
            ]



scanners = []
with open("day19.in") as f:
    scanner = []
    for line in f:
        if line.startswith("---"):
            if scanner:
                scanners.append(scanner)
                scanner = []
        elif line.strip():
            scanner.append(tuple(int(i) for i in line.strip().split(",")))
    scanners.append(scanner)

# print(scanners)
# pprint(list(rotations(scanners[0])))
# print(len(list(rotations(scanners[0]))))


# overlaps = {} # {(sc0, sc1): (x, y, z)}
# overlapping_rotations = {} # {(sc0, sc1): rotation}
# for (idx1, scanner1), (idx2, scanner2) in combinations(enumerate(scanners), 2):
#     for rotation2 in rotations2(scanner2):
#         xyz_diffs = Counter()
#         for beacon1 in scanner1:
#             for beacon2 in rotation2:
#                 xyz_diff = tuple(b - a for b, a in zip(beacon2, beacon1))
#                 xyz_diffs[xyz_diff] += 1
#         most_common = xyz_diffs.most_common(1)[0]
#         if most_common[1] >= 12:
#             print(f"{idx1} overlaps with {idx2} (at {most_common[0]})")
#             overlaps[(idx1, idx2)] = tuple(-i for i in most_common[0])
#             overlapping_rotations[(idx1, idx2)] = rotation2


# print(overlaps)


# relative_to_0 = {0: (0, 0, 0)}
# while len(relative_to_0) < len(scanners):
#     for (idx0, idx1), offset in overlaps.items():
#         if idx1 not in relative_to_0 and idx0 in relative_to_0:
#             relative_to_0[idx1] = tuple(
#                 offset[i] - relative_to_0[idx0][i]
#                 for i in range(len(offset))
#             )

# print(relative_to_0)


# i think instead of doing all this it should just be a tree search or smth
# btw it is 2am

correct_rotations = {0: scanners[0]}
overlaps = {}
positions = {0: (0, 0, 0)}
while len(correct_rotations) < len(scanners):
    items = list(correct_rotations.items())
    for idx1, scanner1 in items:
        for idx2, scanner2 in enumerate(scanners):
            if idx2 not in correct_rotations:
                for rotation2 in rotations(scanner2):
                    xyz_diffs = Counter()
                    for beacon1 in scanner1:
                        for beacon2 in rotation2:
                            xyz_diff = tuple(b - a for b, a in zip(beacon2, beacon1))
                            xyz_diffs[xyz_diff] += 1
                    most_common = xyz_diffs.most_common(1)[0]
                    if most_common[1] >= 12:
                        #print(f"{idx1} overlaps with {idx2} (at {most_common[0]})")
                        overlaps[(idx1, idx2)] = tuple(-i for i in most_common[0])
                        positions[idx2] = tuple(
                            b - a
                            for b, a in zip(positions[idx1], most_common[0])
                        )
                        correct_rotations[idx2] = rotation2

# print(overlaps)
# print(positions)


beacons = set()
for idx, rotation in correct_rotations.items():
    for beacon in rotation:
        beacons.add(
            tuple(
                a + b
                for b, a in zip(beacon, positions[idx])
            )
        )

#pprint(beacons)
print(len(beacons))


# part 2
maxdist = 0
for b1 in positions.values():
    for b2 in positions.values():
        distance = (
            abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])
        )
        if distance > maxdist:
            maxdist = distance

print(maxdist)
