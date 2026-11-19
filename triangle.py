from __future__ import annotations

from typing import Optional, Tuple

from shape import Shape
from vector2d import Vector2D

Point = Tuple[float, float]


class Triangle(Shape):

    def __init__(self, a: Point, b: Point, c: Point):

        # a triangle have 3 corners, each is a point -> it have (x,y) tuple

        self.a: Point = a
        self.b: Point = b
        self.c: Point = c

    # ------------------------------------------------------------------
    # Shape interface – to be implemented
    # ------------------------------------------------------------------
    def get_min_surrounding_point(self) -> Point:
        #The objective is to return  the buttom-left corner of SMALLEST box to be a triangle.
        #Untilizing min!!
        min_x = min(self.a[0], self.b[0], self.c[0])  # This take the smallest x points of angles x, y, z..
        min_y = min(self.a[1], self.b[1], self.c[1]) # Same thing bbut min for y instead
        return (min_x, min_y) # return back the min found

        #raise NotImplementedError

    def get_max_surrounding_point(self) -> Point:
        #This is the oposit of min, same idea, getting the max values
        max_x = max(self.a[0], self.b[0], self.c[0])
        max_y = max(self.a[1], self.b[1], self.c[1])
        return (max_x, max_y)
        #raise NotImplementedError

    def get_center(self) -> Point:
        # The objectiev is to get the centriod. To do so, I would need the average of 3 corner so if we all add side and divide it by 3
        #Same idea as max and min, appplying to all slides
        center_x = (self.a[0] + self.b[0] + self.c[0]) / 3
        center_y = (self.a[1] + self.b[1] + self.c[1]) / 3
        return (center_x, center_y)
        #raise NotImplementedError

    def find_intersection(self, origin: Point, direction: Vector2D) -> Optional[Point]:
        #setting up orgin and direction for later use
        ox, oy = origin
        dx, dy = direction.x, direction.y

        # checking the best so far, making sure to start with None
        best_length_to_origin = None
        best_point = None

        #Going from corner to corner ( a to B, b to c, c to a)
        for (ax, ay), (bx, by) in ((self.a, self.b), (self.b, self.c), (self.c, self.a)):
            #formula B -A -> getting edge direction
            edge_x, edge_y = bx - ax, by - ay
            denominator = dx * edge_y  - dy * edge_x ## is the cross prodyce of the dirction and edge dirction. Measure how much the line cros -> small, large => parrelle = 0
            if denominator == 0:
                continue

            vector_x, vector_y = ax - ox, ay - oy #vectotr from orgin to the start of corner A

            ray_distance = (vector_x * edge_y - vector_y * edge_x) / denominator # will part of forumla -> point = origin + ray_distance x distance
            ray_land = (vector_x * dy - vector_y * dx) / denominator# will be part of formula for edge as point = A + ray_land x (B -A)
            if ray_distance >= 0 and 0 <= ray_land <= 1:
                if best_length_to_origin is None or ray_distance < best_length_to_origin:
                    best_length_to_origin = ray_distance
                    best_point = (ox + ray_distance * dx, oy + ray_distance * dy)
            #print("edge", (ax, ay), (bx, by), "denom", denominator, "t", ray_distance, "u", ray_land)
        return best_point


        #raise NotImplementedError

    def contains_point(self, point: Point) -> bool:
        #objective, is poing inside of the triangle including inside the edge?
        #Utilizing cross product sign test

        #px, py = point.x, point.y
       # ax, ay = self.a.x, self.a.y
        #bx, by = self.b.x, self.b.y
        #cx, cy = self.c.x, self.c.y
        # Crashed beacuse tuple, --> tuple [float, float]

        px, py = point
        ax, ay = self.a
        bx, by = self.b
        cx, cy = self.c

        #Formula -> (end - start) × (point - start) -> (B − A) × (P − A) --> = (Bx − Ax)(Py − Ay) − (By − Ay)(Px − Ax)
        edge1 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        edge2 = (cx - bx) * (py - by) - (cy - by) * (px - bx)
        edge3 = (ax - cx) * (py - cy) - (ay - cy) * (px - cx)
        is_negative = edge1 < 0 or edge2 < 0 or edge3 < 0
        is_positive = edge1 > 0 or edge2 > 0 or edge3 > 0
        return not (is_negative and is_positive)

        #raise NotImplementedError

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