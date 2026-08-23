from __future__ import annotations

from typing import Optional, Tuple

from shape import Shape
from vector2d import Vector2D

Point = Tuple[float, float]


class Triangle(Shape):

    def __init__(self, a: Point, b: Point, c: Point):
        self.a: Point = a
        self.b: Point = b
        self.c: Point = c

    # ------------------------------------------------------------------
    # Shape interface – to be implemented
    # ------------------------------------------------------------------
    def get_min_surrounding_point(self) -> Point:
        raise NotImplementedError

    def get_max_surrounding_point(self) -> Point:
        raise NotImplementedError

    def get_center(self) -> Point:
        raise NotImplementedError

    def find_intersection(self, origin: Point, direction: Vector2D) -> Optional[Point]:
        raise NotImplementedError

    def contains_point(self, point: Point) -> bool:
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"Triangle({self.a}, {self.b}, {self.c})"

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return self.a == other.a and self.b == other.b and self.c == other.c

    def __hash__(self):
        return hash((self.a, self.b, self.c)) 