from __future__ import annotations

import enum
import typing as t


Point: t.TypeAlias = float
Degree: t.TypeAlias = float


class Axis(enum.Enum):
    x = enum.auto()
    y = enum.auto()


__all__ = [
    'Axis', 'Point', 'Degree'
]
