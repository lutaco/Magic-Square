from __future__ import annotations

import copy
import itertools

from shapely.geometry import Polygon
from itertools import combinations
from operator import attrgetter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PltPolygon
import math

from fragments.fragments import Fragment
from .common import Degree
from .fragments import Coord


class FComparable(float):

    def __eq__(self, other):
        return math.fabs(self - other) < 0.1


def _correct_sin_angle(angle, coord):
    if coord.x >= 0 and coord.y >= 0:
        return angle
    if coord.x < 0 <= coord.y:
        return math.pi - angle
    if coord.x <= 0 and coord.y <= 0:
        return math.pi - angle
    if coord.x >= 0 >= coord.y:
        return math.pi * 2 + angle


def angle_between(a: Coord, c: Coord, b: Coord) -> Degree:

    a -= c
    b -= c
    ma = math.sqrt(a.x * a.x + a.y * a.y)
    mb = math.sqrt(b.x * b.x + b.y * b.y)

    angle_a = _correct_sin_angle(math.asin(a.y / ma), a)
    angle_b = _correct_sin_angle(math.asin(b.y / mb), b)

    return angle_b - angle_a


def cycle_with_prev(iterable):
    lst = list(iterable)
    prev = lst[-1]
    for item in lst:
        yield prev, item
        prev = item


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
    target_fragment.rotate2d(-degree, dist_coord)


def centroid(coords):
    xs, ys = zip(*map(attrgetter('x', 'y'), coords))
    return Coord(sum(xs) / len(coords), sum(ys) / len(coords))


def has_collision(*figures):
    for a, b in combinations(figures, 2):
        if IOU(a, b) > 0.1:
            return True
    return False


def delta(iterable):
    lst = list(iterable)
    return max(lst) - min(lst)


def IOU(a_coords, b_coords):
    polygon1_shape = Polygon([(c.x, c.y) for c in a_coords.coords])
    polygon2_shape = Polygon([(c.x, c.y) for c in b_coords.coords])
    return polygon1_shape.intersection(polygon2_shape).area


def shapes(*figures):
    all_coords = itertools.chain.from_iterable(fig.coords for fig in figures)
    xs, ys = zip(*map(attrgetter('x', 'y'), all_coords))
    return delta(xs), delta(ys)


def draw_figures(*figures):
    ax = plt.gca()

    for figure in figures:
        coords = figure.coords
        pts = np.array([(c.x, c.y) for c in coords])
        p = PltPolygon(pts, closed=True, fc='#ff981d', ec="#a53e12")
        ax.add_patch(p)

    xs, ys = shapes(*figures)
    ax.set_aspect(ys / ys)
    ax.autoscale(enable=True, axis='both', tight=None)

    plt.show()


def square_by_points(a: Coord, c: Coord):
    center = centroid([a, c])
    b = copy.deepcopy(a)
    b.rotate(math.pi / 2, center)
    d = copy.deepcopy(c)
    d.rotate(math.pi / 2, center)
    return Fragment([a, b, c, d])


def equals_area(master: Fragment, to_comp: Fragment):
    p = Polygon(to_comp.xy)
    m = Polygon(master.xy)
    return FComparable(p.intersection(m).area) == FComparable(m.area)\
        and FComparable(p.area) == FComparable(m.area)
