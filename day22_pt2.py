from sympy import S, Interval, FiniteSet, ProductSet, Union, pprint, evaluate
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


reboot_steps = []
pattern = re.compile(r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
with open("day22.in") as f:
    for line in f:
        state, xmin, xmax, ymin, ymax, zmin, zmax = pattern.match(line).groups()
        reboot_steps.append(RebootStep(
            state == "on", int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)
        ))


on = S.EmptySet * S.EmptySet * S.EmptySet
nsteps = len(reboot_steps)
for index, step in enumerate(reboot_steps):
    pprint(on)
    print(f"{index+1}/{nsteps}")
    ps = ProductSet(
        Interval(step.xmin, step.xmax) & S.Integers,
        Interval(step.ymin, step.ymax) & S.Integers,
        Interval(step.zmin, step.zmax) & S.Integers,
    )
    with evaluate(False):
        if step.state:
            on += ps
        else:
            on -= ps

pprint(on)
print(len(on))
