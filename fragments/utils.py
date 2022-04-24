from __future__ import annotations

import itertools
from itertools import combinations
from operator import attrgetter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import typing as t
import math

from fragments.fragments import Fragment
from .common import Degree
from .fragments import Coord


def angle_between(a: Coord, b: Coord, c: Coord) -> Degree:
    ax, ay = a.x - b.x, a.y - b.y
    bx, by = c.x - b.x, c.y - b.y

    ma = math.sqrt(ax * ax + ay * ay)
    mb = math.sqrt(bx * bx + by * by)
    sc = ax * bx + ay * by
    res = math.acos(sc / ma / mb)
    res = res if math.acos(ax / ma) > math.acos(bx / mb) else -res
    return res if math.asin(ay / ma) < math.asin(by / mb) else -res


def cycle_with_prev(iterable):
    lst = list(iterable)
    prev = lst[-1]
    for item in lst:
        yield prev, item
        prev = item


def in_fragment(target: Coord, coords: t.List[Coord]):
    c = 0
    x, y = target.x, target.y
    for prev, cur in cycle_with_prev(coords):
        if (cur.y <= y < prev.y or prev.y <= y < cur.y) \
                and (x > (prev.x - cur.x) * (y - cur.y) / (prev.y - cur.y) + cur.x):
            c = 1 - c
    return bool(c)


def connect_fragment(
        target_fragment: Fragment,
        dist_fragment: Fragment,
        target_coord_index,
        dist_cord_index,
        target_helper_coord_index,
        dist_helper_coord_index,
):
    source_coord = target_fragment.coords[target_coord_index]
    dist_coord = dist_fragment.coords[dist_cord_index]

    target_fragment.move(source_coord - dist_coord)

    degree = angle_between(
        dist_fragment.coords[dist_helper_coord_index],
        dist_coord,
        target_fragment.coords[target_helper_coord_index]
    )
    target_fragment.rotate2d(-degree, source_coord)


def has_collision(*figures):
    for a, b in combinations(figures, 2):
        for coord in a.coords:
            if in_fragment(coord, b.coords):
                return True
    return False


def _delta(iterable):
    lst = list(iterable)
    return max(lst) - min(lst)


def draw_figures(*figures):
    ax = plt.gca()

    for figure in figures:
        coords = figure.coords
        pts = np.array([(c.x, c.y) for c in coords])
        p = Polygon(pts, closed=True, fc='#ff981d', ec="#a53e12")
        ax.add_patch(p)

    all_coords = itertools.chain.from_iterable(fig.coords for fig in figures)
    xs, ys = zip(*map(attrgetter('x', 'y'), all_coords))
    ax.set_aspect(_delta(ys) / _delta(xs))
    ax.autoscale(enable=True, axis='both', tight=None)

    plt.show()
