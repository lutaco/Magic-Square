from __future__ import annotations

from fragments import Fragment, Coord, draw_figures
from fragments.utils import connect_fragment, cycle_with_prev


def create_fragment():
    return Fragment([
        Coord(0.0, 0.0),
        Coord(7.0, 0.0),
        Coord(8.5, -8.5),
        Coord(0, -10.0)
    ])


if __name__ == '__main__':

    figures = [create_fragment() for _ in range(4)]
    iterable = cycle_with_prev(figures)

    next(iterable)

    for prev, current in iterable:
        connect_fragment(
            target_fragment=current,
            dist_fragment=prev,
            dist_cord_index=1,
            dist_helper_coord_index=2,
            target_coord_index=3,
            target_helper_coord_index=2,
        )

    draw_figures(*figures)
