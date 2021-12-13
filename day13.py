from collections import namedtuple
from typing import Union

XFold = namedtuple("XFold", "x")
YFold = namedtuple("YFold", "y")
Fold = Union[XFold, YFold]


def fold(dots, fold: Fold):
    new_dots = set()
    for dot in dots:
        if isinstance(fold, XFold):
            if dot[0] < fold.x:
                new_dots.add(dot)
            else:
                new_x = fold.x - (dot[0] - fold.x)
                new_dots.add((new_x, dot[1]))
        elif isinstance(fold, YFold):
            if dot[1] < fold.y:
                new_dots.add(dot)
            else:
                new_y = fold.y - (dot[1] - fold.y)
                new_dots.add((dot[0], new_y))
    return new_dots



def print_dots(dots):
    max_x = max(dots, key=lambda dot: dot[0])[0]
    max_y = max(dots, key=lambda dot: dot[1])[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) not in dots:
                print(".", end="")
            else:
                print("#", end="")
        print()


dots = set()
folds = []
with open("day13.in") as f:
    for line in f:
        if line.startswith("fold along"):
            if "x" in line:
                folds.append(XFold(int(line.strip().split("=")[1])))
            elif "y" in line:
                folds.append(YFold(int(line.strip().split("=")[1])))
        elif not line.strip():
            pass
        else:
            a, b = line.strip().split(",")
            dots.add((int(a), int(b)))


new_dots = fold(dots, folds[0])
print(len(new_dots))


for fold_ in folds:
    dots = fold(dots, fold_)
print_dots(dots)
