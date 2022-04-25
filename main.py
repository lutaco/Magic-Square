from __future__ import annotations

import itertools

from fragments import (
    Fragment, Coord, draw_figures, connect_fragment,
    cycle_with_prev, has_collision, square_by_points, equals_area
)


def round_dem(index):
    return index % 4


def create_fragment(rotate=0, side='top'):
    if side == 'top':
        coords = [
            Coord(0.0, 0.0),
            Coord(7.0, 0.0),
            Coord(8.5, -8.5),
            Coord(0.0, -10.0)
        ]
    else:
        coords = [
            Coord(0.0, 10.0),
            Coord(8.5, 8.5),
            Coord(7.0, 0.0),
            Coord(0.0, 0.0)
        ]

    coords = coords * 2
    return Fragment(coords[rotate:rotate + 4])


if __name__ == '__main__':

    for rotations in itertools.product(range(4), repeat=4):

        for sides in itertools.combinations_with_replacement(['top', 'bottom'], 4):
            figures = [
                create_fragment(rotate, side)
                for rotate, side in zip(rotations, sides)
            ]

            iterable = cycle_with_prev(figures)
            next(iterable)

            for prev, current in iterable:
                connect_fragment(
                    target_fragment=current,
                    dist_cord_index=1,
                    dist_helper_coord_index=2,
                    target_coord_index=3,
                    target_helper_coord_index=2,
                    dist_fragment=prev,
                )

            if not has_collision(*figures):
                figure = Fragment(itertools.chain.from_iterable(fig.coords[:2] for fig in figures))
                square = square_by_points(figures[0].coords[0], figures[2].coords[0])
                if equals_area(figure, square):
                    draw_figures(*figures)
