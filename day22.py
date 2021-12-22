from dataclasses import dataclass
import re


@dataclass
class RebootStep:
    state: bool
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int



def switch_grid(step, grid):
    for z in range(step.zmin, step.zmax+1):
        for y in range(step.ymin, step.ymax+1):
            for x in range(step.xmin, step.xmax+1):
                grid[z+50][y+50][x+50] = step.state


def count_on(grid):
    count = 0
    for z in range(101):
        for y in range(101):
            for x in range(101):
                if grid[z][y][x]:
                    count += 1
    return count


reboot_steps = []
pattern = re.compile(r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
with open("day22.in") as f:
    for line in f:
        state, xmin, xmax, ymin, ymax, zmin, zmax = pattern.match(line).groups()
        reboot_steps.append(RebootStep(
            state == "on", int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)
        ))


#print(reboot_steps)


grid = [
    [
        [
            False
            for x in range(101)
        ]
        for y in range(101)
    ]
    for z in range(101)
]


for step in reboot_steps:
    if (
        -50 <= step.xmin <= 50
        and -50 <= step.xmax <= 50
        and -50 <= step.ymin <= 50
        and -50 <= step.ymax <= 50
        and -50 <= step.zmin <= 50
        and -50 <= step.zmax <= 50
    ):
        switch_grid(step, grid)
print(count_on(grid))
