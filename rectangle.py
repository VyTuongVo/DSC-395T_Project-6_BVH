from __future__ import annotations

from typing import Tuple, Optional

from shape import Shape
from vector2d import Vector2D

Point = Tuple[float, float]


class Rectangle(Shape):
    """Axis-aligned bounding box used by the BVH. This starter version only contains
    the public API signatures"""

    def __init__(self, min_pos: Point, max_pos: Point):
        self.min_pos: Point = min_pos
        self.max_pos: Point = max_pos

    # ---------------------------------------------------------------
    # Shape interface – to be implemented
    # ---------------------------------------------------------------
    def get_min_surrounding_point(self) -> Point:  # noqa: D401
        raise NotImplementedError

    def get_max_surrounding_point(self) -> Point:  # noqa: D401
        raise NotImplementedError

    def get_center(self) -> Point:
        raise NotImplementedError

    def find_intersection(self, origin: Point, direction: Vector2D) -> Optional[Point]:
        raise NotImplementedError

    def contains_point(self, point: Point) -> bool:
        raise NotImplementedError

    # ---------------------------------------------------------------
    # Additional helpers needed by BVH – to be implemented
    # ---------------------------------------------------------------
    def does_ray_intersect(self, origin: Point, direction: Vector2D) -> bool:
        raise NotImplementedError