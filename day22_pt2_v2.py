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


def step_interval(step):
    return ProductSet(
        Interval(step.xmin, step.xmax),
        Interval(step.ymin, step.ymax),
        Interval(step.zmin, step.zmax),
    )


reboot_steps = []
pattern = re.compile(r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
with open("day22.in") as f:
    for line in f:
        state, xmin, xmax, ymin, ymax, zmin, zmax = pattern.match(line).groups()
        reboot_steps.append(RebootStep(
            state == "on", int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)
        ))


on_count = 0
nsteps = len(reboot_steps)
for index, step in enumerate(reboot_steps):
    print(f"{index+1}/{nsteps} = {on_count}")
    ps = step_interval(step)
    #num_on = len(ps)
    mod_ps = ps
    if step.state:
        later_turned_off = S.EmptySet * S.EmptySet * S.EmptySet
        for step2 in reboot_steps[index::-1]:
            if step2 == step: continue
            ps2 = step_interval(step2)
            # if step2 turned the things off, then we should turn them on
            # if step2 turned the things on, then we shouldn't turn them on again,
            # unless they were turned off later
            if step2.state:
                print("a")
                mod_ps -= (ps2 - later_turned_off)
                print("b")
            else:
                print("c")
                later_turned_off += (ps2 & ps)
                print("d")
        on_count += mod_ps.measure
    else:
        later_turned_on = S.EmptySet * S.EmptySet * S.EmptySet
        for step2 in reboot_steps[index::-1]:
            if step2 == step: continue
            ps2 = step_interval(step2)
            # if step2 turned the things on, then we should turn them off
            # if step2 turned the things off, then we shouldn't turn them off again
            if not step2.state:
                mod_ps -= (ps2 - later_turned_on)
            else:
                later_turned_on += (ps2 & ps)
        on_count -= mod_ps.measure


print(on_count)