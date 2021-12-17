import re
from itertools import count

pattern = re.compile(r"target area: x=([0-9\-]+)..([0-9\-]+), y=([0-9\-]+)..([0-9\-]+)")

with open("day17.in") as f:
    line = f.readline().strip()

xmin, xmax, ymin, ymax = (int(i) for i in pattern.match(line).groups())

# steps (gonna math this one)
# x(0) = 0
# y(0) = 0
# x(t) = x(t-1) + xvel(t)
# y(t) = y(t-1) + yvel(t)
# xvel(t) = xvel(t-1) - 1 if xvel > 0;
#           xvel(t-1) + 1 if xvel < 0;
#           xvel(t-1) if xvel = 0
# yvel(t) = yvel(t-1) - 1
# xvel(0) = ?
# yvel(0) = ?
# i don't think i'm approaching this the right way


# i think a good first step is to bruteforce this maybe

def lands_in_target(xvel0, yvel0):
    x = 0
    y = 0
    xvel = xvel0
    yvel = yvel0
    peak = y
    while True:
        x = x + xvel
        y = y + yvel
        peak = max(y, peak)
        if xvel > 0:
            xvel = xvel - 1
        elif xvel < 0:
            xvel = xvel + 1
        yvel = yvel - 1
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True, peak
        if y < ymin:
            return False, peak



try:
    maxy = 0
    for yvel0 in count(0):
        # hypothesis: if there are none it's done (wrong)
        done = True
        for xvel0 in range(0, xmax):
            result, peak = lands_in_target(xvel0, yvel0)
            if result:
                maxy = max(peak, maxy)
                done = False
        print(maxy)
except KeyboardInterrupt:
    print("Interrupting")

print(maxy)

input("press enter to continue")


# pt2

try:
    initvels = set()
    for yvel0 in count(ymin):
        for xvel0 in range(0, xmax+500):  # idk
            result, peak = lands_in_target(xvel0, yvel0)
            if result:
                initvels.add((xvel0, yvel0))
        print(len(initvels))
except KeyboardInterrupt:
    print("Interrupting")

print(initvels)
