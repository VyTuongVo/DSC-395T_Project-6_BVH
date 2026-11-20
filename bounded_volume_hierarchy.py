from __future__ import annotations

from typing import List, Set, Tuple, Optional

from bvh import BVH, SplitMethod
from shape import Shape
from vector2d import Vector2D
from rectangle import Rectangle

Point = Tuple[float, float]

# since we are wokring and creating a tree, I would need to create node class

class BoundedVolumeHierarchy(BVH):

    # since we are wokring and creating a tree, I would need to create node class
    class Node:
        def __init__(self, box, shape = None, right = None, left = None, height = 0):
            self.shape = shape
            self.right = right
            self.left = left
            self.box = box
            self.height = height

        def leaves(self) -> bool: #Is this node a leaf?
            return self.shape is not None

    def __init__(self):
        self._split_method: SplitMethod = SplitMethod.SPLIT_MEDIAN
        self._root = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    @staticmethod
    def box_shape(shape) -> Rectangle:
        min_point = shape.get_min_surrounding_point()
        max_point = shape.get_max_surrounding_point()
        return Rectangle(min_point, max_point)

    @staticmethod
    def box_combination (box1: Rectangle, box2: Rectangle) -> Rectangle:
        min_x1, min_y1 = box1.min_pos
        min_x2, min_y2 = box2.min_pos
        max_x1, max_y1 = box1.max_pos
        max_x2, max_y2 = box2.max_pos

        new_min = (min(min_x1, min_x2), min(min_y1, min_y2))
        new_max = (max(max_x1, max_x2), max(max_y1, max_y2))
        return Rectangle(new_min, new_max)

    def set_split_method(self, split_method: SplitMethod) -> None:
        # TODO: implement
        self._split_method = split_method
        #raise NotImplementedError

    # ------------------------------------------------------------------
    # Construction & mutation
    # ------------------------------------------------------------------
    def build_bvh(self, shape_list: List[Shape]) -> None:
        # TODO: implement
        #if shape_list is None:
        if not shape_list:
            self._root = None # If the list is empty, please return
            return
        def build(shapes, depth): # Creating in order to build recurrsion!
            if len(shapes) == 1: #1 triangle, make it a leaf! --> defualt mode!
                shape = shapes[0]
                return self.Node(self.box_shape(shape), shape) # send it back to the node and create a leaf out of it!
            axis = depth % 2  # --> (0,1)
            # Objective: sort the triangles by their center on the current axis (x or y), keeping track of each one's position so we can rebuild the list in order
            pair = []
            for i in range(len(shapes)):
                pair.append((shapes[i].get_center()[axis], i))
            pair.sort()

            shape_list_sort = []
            for value, i in pair:
                shape_list_sort.append(shapes[i])
            #objective is to cute the sorted list in half,
            mid_point = len(shape_list_sort) // 2
            left_list = shape_list_sort[:mid_point]
            right_list = shape_list_sort[mid_point:]

            #build a subtree for each half ->. to do so depth + 1
            left = build(left_list, depth + 1)
            right = build(right_list, depth + 1)

            #make parent node that break to bold both half
            box = self.box_combination(left.box, right.box)
            height = 1 + max(left.height, right.height)
            return self.Node(box, left = left, right = right, height = height)

        self._root = build(shape_list, depth = 0)
        #raise NotImplementedError


        #objevtive is if x is left heavy, then move its lefy child up to the top
        #ex:        A                B
        #       B       C -->    D      A
        #    D     E                 E       C
    def right_rotation(self,A):
        B = A.left

        #Rotating and chnage A over to B ->> chnaging position
        A.left = B.right
        B.right = A

        # recomptuing A and where it goes in the tree
        A.box = self.box_combination(A.left.box, A.right.box)
        A.height = 1 + max(A.left.height, A.right.height)

        #Recomputing B based on A
        B.box = self.box_combination(B.left.box, B.right.box)
        B.height = 1 + max(B.left.height, B.right.height)

        return B

    def left_rotation(self,A):
        #Objective is to move right child C up to the top
        C = A.right

        #rotating D over to where A is and where A is under C
        A.right = C.left
        C.left = A

        #Recimputing A
        A.box = self.box_combination(A.left.box, A.right.box)
        A.height = 1 + max(A.left.height, A.right.height)

        # Recompiting C based on A
        C.box = self.box_combination(C.left.box, C.right.box)
        C.height = 1 + max(C.left.height, C.right.height)

        return C

    # ObjectiveL if a the AVL rule break, we need to rotate to fix it. Meaning the new top will be return
    def rebalance(self, A):

        if A.leaves(): return A

        else:
            diff_height = A.left.height - A.right.height

            if diff_height > 1:  # Meaning that the left is too tsll
                B = A.left
                if B.right.height > B.left.height: #if the inside is taller
                    A.left = self.left_rotation(B)
                return self.right_rotation(A)
            elif diff_height < -1: #right is too tall
                C = A.right
                if C.left.height > C.right.height: A.right = self.right_rotation(C)
                return self.left_rotation(A)
            return A

    #ObjectieL decide whether the new trinagle goas left or right using the 4 rueles provided.
    # - Leave first, less box growth, shotern height, and random. --> use ONLY if the rules aboves are tied

    def chosen_child (self, node, new_box):
        left = node.left
        right = node.right

        #Rule 1: -> leaves first

        if left.leaves() and not right.leaves(): return left
        if right.leaves() and not left.leaves(): return right


        #Rule 2 -> Less permater expension --> Using the perimter formula of 2 (width + height)

        # Left side
        min_x, min_y = left.box.min_pos
        max_x, max_y = left.box.max_pos
        #caculating current left child
        current_left = 2 * ((max_x - min_x) + (max_y - min_y))

        #Calcualting after adding new trinagle

        left_combined = self.box_combination(left.box, new_box)
        min_x, min_y = left_combined.min_pos
        max_x, max_y = left_combined.max_pos
        after_left = 2 * ((max_x - min_x) + (max_y - min_y))

        #Right Side - current
        min_x, min_y = right.box.min_pos
        max_x, max_y = right.box.max_pos
        current_right = 2 * ((max_x - min_x) + (max_y - min_y))

        # right side (chikld) after
        right_combined = self.box_combination(right.box, new_box)
        min_x, min_y = right_combined.min_pos
        max_x, max_y = right_combined.max_pos
        after_right = 2 * ((max_x - min_x) + (max_y - min_y))

        left_different = after_left - current_left
        right_different = after_right - current_right
        if left_different < right_different: return left
        if right_different < left_different: return right

        # Rule 3 -< shotr hieght of tree

        if left.height < right.height: return left
        if right.height < left.height: return right

        #Rule 4: random
        return random.choice([left, right])

    def insert(self, shape: Shape) -> None:

        # TODO: implement
        # Objecive - adding trinaging to ree and then fixing box and high to make sure eeverthing balace out

        new_leaf = self.Node(self.box_shape(shape), shape=shape)

        if self._root is None:
            self._root = new_leaf
            return

        def locate(node):
            if node.leaves():
                box = self.box_combination(node.box, new_leaf.box)
                return self.Node(box, left=node, right=new_leaf, height=1) # box will provide the surround trinagle, node will give new leave so that its not a child, and right will give new leaf making it a new trinagle.

            chosen_child = self.chosen_child(node, new_leaf.box)
            if chosen_child is node.left:
                node.left = locate(node.left)
            else:
                node.right = locate(node.right)

            node.box = self.box_combination(node.left.box, node.right.box)
            node.height = 1 + max(node.left.height, node.right.height)
            return self.rebalance(node)

        self._root = locate(self._root)
    #raise NotImplementedError

    def remove(self, shape: Shape) -> None:
        # TODO: implement
    #ObjectiveL remove one triangle, then fix the boxes in based on hieght and balancing the tree

        # empty tree -> nothing to do so we return
        if self._root is None:
            return

        #create the triangle's box
        targeted_box = self.box_shape(shape)

        def delete(node):
            status = False
            if node.leaves():
                if node.shape == shape: # if the triangle stored in this leaf the same triange we're trying to remove?
                    status = True
                    return None, status
                return node, status

            #If the traingle's box ins't inside the node's box -> then return false
            if not (node.box.contains_point(targeted_box.min_pos) and node.box.contains_point(targeted_box.max_pos)):
                return node, status #return status as false

            #searching between left and right

            #search left
            new_left, status = delete(node.left)
            if status:
                if new_left is None: #if the left child was the removed leaf
                    return node.right, status
                node.left = new_left  #other

            #if its not on the leftn it a right search
            else:
                new_right, status = delete(node.right)
                if not status:
                    return node, status
                if new_right is None:
                    return node.left, status
                node.right = new_right


            #fix box and hieght and then rebalance
            node.box = self.box_combination(node.left.box, node.right.box)
            node.height = 1 + max(node.left.height, node.right.height)
            return self.rebalance(node), status

        self._root, status = delete(self._root)






        #raise NotImplementedError

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def find_collision(self, point: Point) -> Set[Shape]:
        # TODO: implement
        result = set()
        #stack = [(self._root, 0)] # 'tuple' object has no attribute 'box'
        stack = [self._root]
        while stack:
            node = stack.pop()
            if node is None: #if there is nothing in node, continue -> if not break
                continue
            if not node.box.contains_point(point): # Skip branch if the point isn't in the node's box
                continue
            if node.leaves(): #if the node is in leaf, then add into result to print later
                if node.shape.contains_point(point):
                    result.add(node.shape)
            else:
                #stack.append((self._root, depth + 1))
                stack.append(node.left)
                stack.append(node.right)
        return result

        #raise NotImplementedError

    def intersect_ray(self, origin: Point, direction: Vector2D) -> Optional[Shape]:
        # TODO: implement
        #objective: return the cloest trianger that hit or return none if there is nothing

        best = None
        best_distance = None
        stack = [self._root]
        while stack:
            node = stack.pop()
            if node is None: continue # skip node if its empty
            if not node.box.does_ray_intersect(origin, direction):continue # skip the branch if the ray doesn't have node's box

            if node.leaves(): #if there is leave
                hit = node.shape.find_intersection(origin, direction) # it check the triangle 3 edges and it will store points
                if hit is not None: # as long as hit is not 0, then do look at the point distnce and make it my distance
                    point_distance  = self.distance_between_points(origin, hit)  # Call in to dtermine the distane between the points
                    if best_distance is None or point_distance < best_distance:
                        best_distance = point_distance
                        best = node.shape

            else:
                stack.append(node.right)
                stack.append(node.left)

        return best

        #raise NotImplementedError

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------
    def __str__(self) -> str:  # noqa: Dunder missing
        # TODO: implement

        #turning treet into text -> will return a string with 1 line per node
        return_line = []

        stack = [(self._root, 0)] #(NODE, DEpth)
        while stack:
            node, depth = stack.pop() # take the last one and pop it
            if node is None:
                continue
            else:
                tabs = "\t" * depth

            if node.leaves():
                return_line.append(tabs + f"{node.shape.a} {node.shape.b} {node.shape.c}")
            else:
                return_line.append(tabs + f"[{node.box.min_pos}, {node.box.max_pos}]")
                stack.append((node.right, depth + 1))
                stack.append((node.left, depth + 1))
        return "\n".join(return_line)



        raise NotImplementedError
