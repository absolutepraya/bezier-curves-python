import heapq
import itertools
from .core import fit_cubic_bezier, calculate_max_error, chord_length_parameterize
from bezier_math import cubic_bezier

def fit_curves_to_fixed_count(contours, target_count):
    """
    Fits Bezier curves to a list of contours such that the total number of curves
    is approximately target_count.
    
    Uses a priority queue to iteratively split the segment with the highest error.
    """
    # Re-implementation with contour_idx tracking
    return _fit_curves_with_heap(contours, target_count)

def _fit_curves_with_heap(contours, target_count):
    
    class Node:
        def __init__(self, points, contour_idx):
            self.points = points
            self.contour_idx = contour_idx
            self.curve = None
            self.error = -1.0
            self.next = None
            self.prev = None
            
        def fit(self):
            self.curve = fit_cubic_bezier(self.points)
            if self.curve:
                self.error = calculate_max_error(self.points, self.curve)
            else:
                self.error = 0.0

    contour_heads = [None] * len(contours)
    heap = []
    counter = itertools.count()
    total_curves = 0
    
    # Initial fitting
    for i, contour in enumerate(contours):
        if len(contour) < 2:
            continue
        
        node = Node(contour, i)
        node.fit()
        contour_heads[i] = node
        
        if node.curve:
            total_curves += 1
            if len(node.points) >= 4:
                heapq.heappush(heap, (-node.error, next(counter), node))

    # Iteratively split until we reach target_count
    while total_curves < target_count and heap:
        neg_err, _, node = heapq.heappop(heap)
        
        points = node.points
        curve = node.curve
        
        # Split logic
        u = chord_length_parameterize(points)
        max_dist = 0.0
        split_idx = len(points) // 2
        
        # Find the point with maximum error
        for i in range(len(points)):
            p_curve = cubic_bezier(u[i], curve[0], curve[1], curve[2], curve[3])
            dist = points[i].dist(p_curve)
            if dist > max_dist:
                max_dist = dist
                split_idx = i
        
        # Ensure split_idx is valid
        if split_idx == 0: split_idx = 1
        if split_idx == len(points) - 1: split_idx = len(points) - 2
        
        left_points = points[:split_idx+1]
        right_points = points[split_idx:]
        
        left_node = Node(left_points, node.contour_idx)
        right_node = Node(right_points, node.contour_idx)
        left_node.fit()
        right_node.fit()
        
        # Link updates
        left_node.prev = node.prev
        left_node.next = right_node
        right_node.prev = left_node
        right_node.next = node.next
        
        if node.prev:
            node.prev.next = left_node
        else:
            # Node was head
            contour_heads[node.contour_idx] = left_node
            
        if node.next:
            node.next.prev = right_node
            
        total_curves += 1
        
        # Push new nodes to heap if they have enough points
        if left_node.curve and len(left_node.points) >= 4:
            heapq.heappush(heap, (-left_node.error, next(counter), left_node))
        if right_node.curve and len(right_node.points) >= 4:
            heapq.heappush(heap, (-right_node.error, next(counter), right_node))
            
    # Collect results
    all_curves = []
    for head in contour_heads:
        contour_curves = []
        curr = head
        while curr:
            if curr.curve:
                contour_curves.append(curr.curve)
            curr = curr.next
        all_curves.append(contour_curves)
        
    return all_curves
