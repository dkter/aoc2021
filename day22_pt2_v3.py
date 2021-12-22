from sympy import S, Interval, FiniteSet, ProductSet, Union, pprint as sprint, evaluate
from dataclasses import dataclass
from pprint import pprint
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


class _EmptyCube:
    def __or__(self, other):
        if isinstance(other, _EmptyCube):
            return self
        return NotImplemented
EmptyCube = _EmptyCube()


class Cube:
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __or__(self, other):
        # intersect
        if other is EmptyCube:
            return EmptyCube
        # check bounds
        if (
            self.xmax < other.xmin
            or other.xmax < self.xmin
            or self.ymax < other.ymin
            or other.ymax < self.ymin
            or self.zmax < other.zmin
            or other.zmax < self.zmin
        ):
            return EmptyCube
        xmin = max(self.xmin, other.xmin)
        xmax = min(self.xmax, other.xmax)
        ymin = max(self.ymin, other.ymin)
        ymax = min(self.ymax, other.ymax)
        zmin = max(self.zmin, other.zmin)
        zmax = min(self.zmax, other.zmax)
        return Cube(xmin, xmax, ymin, ymax, zmin, zmax)

    def __ror__(self, other):
        if other is EmptyCube:
            return EmptyCube
        else:
            return NotImplemented

    def to_product_set(self):
        return ProductSet(
            Interval(self.xmin, self.xmax+1),
            Interval(self.ymin, self.ymax+1),
            Interval(self.zmin, self.zmax+1),
        )

    def __repr__(self):
        return (
            f"Cube(({self.xmin}, {self.xmax}), ({self.ymin}, {self.ymax}),"
            f" ({self.zmin, self.zmax}))"
        )


class PartialCube(Cube):
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        self.subtracted_cubes = []

    def __isub__(self, other):
        assert isinstance(other, Cube)
        intersection = self | other
        if intersection is not EmptyCube:
            self.subtracted_cubes.append(intersection)

    def get_volume(self):
        base_vol = (
            (self.xmax - self.xmin + 1)
            * (self.ymax - self.ymin + 1)
            * (self.zmax - self.zmin + 1)
        )
        sub_union = Union(*[sc.to_product_set() for sc in self.subtracted_cubes])
        return base_vol - sub_union.measure

    def __repr__(self):
        return (
            f"PartialCube(({self.xmin}, {self.xmax}), ({self.ymin}, {self.ymax}),"
            f" ({self.zmin, self.zmax}) - {self.subtracted_cubes})"
        )



reboot_steps = []
pattern = re.compile(r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
with open("day22.in") as f:
    for line in f:
        state, xmin, xmax, ymin, ymax, zmin, zmax = pattern.match(line).groups()
        reboot_steps.append(RebootStep(
            state == "on", int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)
        ))


cubes = []
nsteps = len(reboot_steps)
for index, step in enumerate(reboot_steps):
    if step.state:
        new_cube = PartialCube(
            step.xmin, step.xmax, step.ymin, step.ymax, step.zmin, step.zmax
        )
        new_cube_full = Cube(
            step.xmin, step.xmax, step.ymin, step.ymax, step.zmin, step.zmax
        )
        for cube in cubes:
            cube -= new_cube_full
        cubes.append(new_cube)
    else:
        sub_cube = Cube(
            step.xmin, step.xmax, step.ymin, step.ymax, step.zmin, step.zmax
        )
        for cube in cubes:
            cube -= sub_cube


total_vol = 0
nsteps = len(cubes)
for index, cube in enumerate(cubes):
    print(f"{index+1}/{nsteps}")
    total_vol += cube.get_volume()
#pprint(cubes)
print(total_vol)
