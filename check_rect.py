from rectangle import Rectangle
from vector2d import Vector2D

r = Rectangle((2, 1), (5, 5))
print(r.get_center())                                   # (3.5, 3.0)
print(r.contains_point((2, 1)))                         # True
print(r.contains_point((6, 3)))                         # False
print(r.does_ray_intersect((0, 0), Vector2D(1, 1)))     # True
print(r.find_intersection((0, 0), Vector2D(1, 1)))      # (2.0, 2.0)
print(r.does_ray_intersect((0, 0), Vector2D(-1, 0)))    # False
print(r.does_ray_intersect((3, 0), Vector2D(0, 1)))     # True
print(r.does_ray_intersect((0, 0), Vector2D(0, 1)))     # False
print(r.find_intersection((3, 3), Vector2D(1, 0)))      # (3, 3)
