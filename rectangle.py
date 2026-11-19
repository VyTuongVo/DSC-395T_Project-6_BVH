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
        return self.min_pos # A rectangle is a bounding box -> 2 corners already stored as min_pos and max_pos
        #raise NotImplementedError

    def get_max_surrounding_point(self) -> Point:  # noqa: D401
        return self.max_pos
        #raise NotImplementedError

    def get_center(self) -> Point:
        min_x, min_y = self.min_pos
        max_x, max_y = self.max_pos
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        return (center_x, center_y)
        #raise NotImplementedError

    def find_intersection(self, origin: Point, direction: Vector2D) -> Optional[Point]:
        ox, oy = origin
        dx, dy = direction.x, direction.y
        min_x, min_y = self.min_pos
        max_x, max_y = self.max_pos

        start_point = 0
        end_point = None

        if dx == 0:
            if ox < min_x or ox > max_x:
                return None
        else:
            start_point_1 = (min_x - ox) / dx
            start_point_2 = (max_x - ox) / dx
            if start_point_1 > start_point_2:
                start_point_1, start_point_2 = start_point_2, start_point_1
            start_point = max(start_point, start_point_1)
            if end_point is None:
                end_point = start_point_2
            else:
                end_point = min(end_point, start_point_2)

        # Copy the same idea to dy
        if dy == 0:
            if oy < min_y or oy > max_y:
                return None
        else:
            end_point_1 = (max_y - oy) / dy
            end_point_2 = (min_y - oy) / dy
            if end_point_1 > end_point_2:
                end_point_1, end_point_2 = end_point_2, end_point_1
            start_point = max(start_point, end_point_1)
            if end_point is None:
                end_point = end_point_2  # earliest exit
            else:
                end_point = min(end_point, end_point_2)

        # didn't move
        if end_point is None:
            if self.contains_point(origin):  # Return origin
                return origin
            return None  # or return none

        # if in box, return
        elif start_point <= end_point:
            return (ox + start_point * dx, oy + start_point * dy)
        else:  # if not inside, then return none
            return None
        #raise NotImplementedError

    def contains_point(self, point: Point) -> bool:
        # Since the point is inside (edge included) if its between the corners on both axes!
        px, py = point
        min_x, min_y = self.min_pos
        max_x, max_y = self.max_pos
        return (min_x <= px <= max_x) and (min_y <= py <= max_y)


        #raise NotImplementedError

    # ---------------------------------------------------------------
    # Additional helpers needed by BVH – to be implemented
    # ---------------------------------------------------------------
    def does_ray_intersect(self, origin: Point, direction: Vector2D) -> bool:
        if self.find_intersection(origin, direction) is None:
            return False
        else:
            return True
        #raise NotImplementedError