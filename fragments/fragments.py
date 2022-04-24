from __future__ import annotations

import typing as t
import math
from dataclasses import dataclass

from fragments.common import Point, Degree, Axis


@dataclass
class CoordDelta:
    x: Point
    y: Point


@dataclass
class Coord:

    x: Point
    y: Point

    def rotate(self, angle: Degree, pivot: Coord = None):
        if pivot is None:
            pivot = Coord(.0, .0)

        ox, oy = pivot.x, pivot.y
        px, py = self.x, self.y

        self.x = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        self.y = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    def swap(self, axis=Axis.x, pivot: Coord = None):
        if pivot is None:
            pivot = Coord(.0, .0)
        if axis == axis.x:
            self.x -= 2 * (self.x - pivot.x)
        elif axis == axis.y:
            self.y -= 2 * (self.y - pivot.y)
        else:
            raise ValueError(f'unknown axis {axis}')

    def __sub__(self, other) -> CoordDelta:
        return CoordDelta(self.x - other.x, self.y - other.y)


class Fragment:

    coords: t.List[Coord]
    main: Coord

    def __init__(self, coords):
        self.coords = coords

    @property
    def main(self):
        return self.coords[0]

    def rotate2d(self, angle: Degree, pivot=None):
        for coord in self.coords:
            coord.rotate(angle, pivot=self.main if pivot is None else pivot)

    def rotate3d(self, axis=Axis.x):
        for coord in self.coords:
            coord.swap(axis, pivot=self.main)

    def __contains__(self, item):
        return item in self.coords

    @property
    def dimension(self):
        return len(self.coords)

    def move(self, delta: CoordDelta):
        for coord in self.coords:
            coord.x -= delta.x
            coord.y -= delta.y
