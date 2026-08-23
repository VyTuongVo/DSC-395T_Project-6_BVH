from __future__ import annotations

from typing import List, Set, Tuple, Optional

from bvh import BVH, SplitMethod
from shape import Shape
from vector2d import Vector2D

Point = Tuple[float, float]


class BoundedVolumeHierarchy(BVH):

    def __init__(self):
        self._split_method: SplitMethod = SplitMethod.SPLIT_MEDIAN

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    def set_split_method(self, split_method: SplitMethod) -> None:
        # TODO: implement
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Construction & mutation
    # ------------------------------------------------------------------
    def build_bvh(self, shape_list: List[Shape]) -> None:
        # TODO: implement
        raise NotImplementedError

    def insert(self, shape: Shape) -> None:
        # TODO: implement
        raise NotImplementedError

    def remove(self, shape: Shape) -> None:
        # TODO: implement
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def find_collision(self, point: Point) -> Set[Shape]:
        # TODO: implement
        raise NotImplementedError

    def intersect_ray(self, origin: Point, direction: Vector2D) -> Optional[Shape]:
        # TODO: implement
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------
    def __str__(self) -> str:  # noqa: Dunder missing
        # TODO: implement
        raise NotImplementedError
