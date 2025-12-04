import math
from bezier_math import Point, cubic_bezier, bernstein_poly

def chord_length_parameterize(points):
    """
    Parameterizes points based on chord length.
    Returns a list of t values corresponding to each point.
    """
    u = [0.0]
    for i in range(1, len(points)):
        dist = points[i].dist(points[i-1])
        u.append(u[-1] + dist)
    
    total_length = u[-1]
    if total_length == 0:
        return [0.0] * len(points)
        
    return [x / total_length for x in u]

def fit_cubic_bezier(points):
    """
    Fits a single cubic Bezier curve to a set of points using Least Squares.
    P0 and P3 are fixed as the first and last points.
    We need to solve for P1 and P2.
    """
    n = len(points)
    if n < 2:
        return None # Not enough points

    p0 = points[0]
    p3 = points[-1]

    if n == 2:
        # Straight line, place control points at 1/3 and 2/3
        p1 = p0 * (2/3) + p3 * (1/3)
        p2 = p0 * (1/3) + p3 * (2/3)
        return [p0, p1, p2, p3]

    # Parameterize points
    u = chord_length_parameterize(points)

    # We want to minimize sum || B(u_i) - P_i ||^2
    # B(u) = (1-u)^3 P0 + 3(1-u)^2 u P1 + 3(1-u) u^2 P2 + u^3 P3
    # Let A1(u) = 3(1-u)^2 u
    # Let A2(u) = 3(1-u) u^2
    # We want to find P1, P2 such that:
    # A1(u_i) P1 + A2(u_i) P2  ~=  P_i - (1-u_i)^3 P0 - u_i^3 P3
    # Let X = [P1, P2]^T (conceptually, solving for x and y separately)
    
    # System of equations:
    # [ sum(A1^2)    sum(A1*A2) ] [ P1 ] = [ sum(A1 * RHS) ]
    # [ sum(A1*A2)   sum(A2^2)  ] [ P2 ]   [ sum(A2 * RHS) ]
    
    c11 = 0.0
    c12 = 0.0
    c22 = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0

    for i in range(n):
        t = u[i]
        a1 = 3 * (1-t)**2 * t
        a2 = 3 * (1-t) * t**2
        
        # RHS vector = P_i - (1-t)^3 P0 - t^3 P3
        b0 = (1-t)**3
        b3 = t**3
        rhs = points[i] - (p0 * b0) - (p3 * b3)
        
        c11 += a1 * a1
        c12 += a1 * a2
        c22 += a2 * a2
        
        x1 += a1 * rhs.x
        x2 += a2 * rhs.x
        y1 += a1 * rhs.y
        y2 += a2 * rhs.y

    # Determinant of the matrix
    det = c11 * c22 - c12 * c12
    
    if abs(det) < 1e-9:
        # Singular matrix, fallback to straight line approximation
        p1 = p0 * (2/3) + p3 * (1/3)
        p2 = p0 * (1/3) + p3 * (2/3)
        return [p0, p1, p2, p3]

    # Inverse matrix multiplication
    # [ P1 ] = (1/det) * [  c22  -c12 ] [ X1 ]
    # [ P2 ]             [ -c12   c11 ] [ X2 ]
    
    p1_x = (c22 * x1 - c12 * x2) / det
    p2_x = (-c12 * x1 + c11 * x2) / det
    
    p1_y = (c22 * y1 - c12 * y2) / det
    p2_y = (-c12 * y1 + c11 * y2) / det
    
    p1 = Point(p1_x, p1_y)
    p2 = Point(p2_x, p2_y)
    
    return [p0, p1, p2, p3]

def calculate_max_error(points, curve):
    """
    Calculates the maximum distance between the points and the fitted curve.
    """
    u = chord_length_parameterize(points)
    max_dist = 0.0
    for i in range(len(points)):
        p_curve = cubic_bezier(u[i], curve[0], curve[1], curve[2], curve[3])
        dist = points[i].dist(p_curve)
        if dist > max_dist:
            max_dist = dist
    return max_dist

def fit_curve_recursive(points, error_threshold=2.0):
    """
    Recursively fits Bezier curves to the points.
    If the error is too large, splits the points and fits again.
    """
    if len(points) < 2:
        return []
        
    curve = fit_cubic_bezier(points)
    if curve is None:
        return []

    max_err = calculate_max_error(points, curve)
    
    if max_err < error_threshold or len(points) < 4:
        return [curve]
    
    # Split points at the point of maximum error
    # To find the split index, we re-evaluate distances
    u = chord_length_parameterize(points)
    max_dist = 0.0
    split_idx = len(points) // 2 # Default split
    
    for i in range(len(points)):
        p_curve = cubic_bezier(u[i], curve[0], curve[1], curve[2], curve[3])
        dist = points[i].dist(p_curve)
        if dist > max_dist:
            max_dist = dist
            split_idx = i
            
    # Ensure we don't split at endpoints
    if split_idx == 0: split_idx = 1
    if split_idx == len(points) - 1: split_idx = len(points) - 2
    
    left_points = points[:split_idx+1]
    right_points = points[split_idx:]
    
    left_curves = fit_curve_recursive(left_points, error_threshold)
    right_curves = fit_curve_recursive(right_points, error_threshold)
    
    return left_curves + right_curves

def fit_curves_to_fixed_count(contours, target_count):
    """
    Fits Bezier curves to a list of contours such that the total number of curves
    is approximately target_count.
    
    Uses a priority queue to iteratively split the segment with the highest error.
    """
    import heapq
    
    # 1. Initial fit: 1 curve per contour
    # Heap stores: (-error, contour_index, points_of_segment, fitted_curve)
    # We use negative error because heapq is a min-heap
    pq = []
    
    # Store the final curves for each contour. 
    # Since we split segments, we need a way to reconstruct the order.
    # A simple way is to keep the segments in a list for each contour, 
    # and when we split, we replace one segment with two.
    # But to use the heap, we need to know which segment to replace.
    
    # Let's define a Segment class or structure
    class Segment:
        def __init__(self, points, curve, error):
            self.points = points
            self.curve = curve
            self.error = error
            
        def __lt__(self, other):
            return self.error > other.error # Max-heap behavior
            
    # Initialize segments for all contours
    all_segments = [] # List of lists of Segments
    
    total_curves = 0
    
    for i, contour in enumerate(contours):
        if len(contour) < 2:
            all_segments.append([])
            continue
            
        curve = fit_cubic_bezier(contour)
        if curve is None:
            all_segments.append([])
            continue
            
        err = calculate_max_error(contour, curve)
        seg = Segment(contour, curve, err)
        all_segments.append([seg])
        total_curves += 1
        
        # Add to priority queue
        # We store (error, contour_index, segment_index_in_list)
        # Note: segment_index_in_list is tricky because list changes.
        # Better: Store the Segment object itself in the heap, and modify the list structure.
        # But we need to know where it came from to split it.
        
    # Let's use a flat list of all active segments that are candidates for splitting.
    # And we need to map them back to contours at the end.
    # Actually, we can just maintain the list of segments per contour.
    # The heap will store (-error, contour_index, segment_index).
    # Wait, if we insert into the middle of a list, indices shift.
    # Linked list? Or just use a unique ID for each segment?
    
    # Alternative:
    # 1. Start with [ (contour_points) ] for each contour.
    # 2. Fit curve to each.
    # 3. Put all valid segments into a heap: (-error, contour_idx, segment_obj)
    # 4. While count < target:
    #    Pop max error segment.
    #    Split points.
    #    Fit left, Fit right.
    #    Replace parent segment with left and right in the contour's segment list.
    #    Push left and right to heap.
    
    # To handle the "replace in list" efficiently without indices messing up:
    # We can use a Node class for a doubly linked list, or just a list and rebuild it?
    # Given N=21 or even 100, list operations are cheap.
    
    # Let's use a wrapper object that knows its position or is part of a linked structure.
    
    class Node:
        def __init__(self, points):
            self.points = points
            self.curve = None
            self.error = -1.0
            self.next = None
            self.prev = None
            
        def fit(self):
            self.curve = fit_cubic_bezier(self.points)
            if self.curve:
                self.error = calculate_max_error(self.points, self.curve)
            else:
                self.error = 0.0 # Cannot split further
                
    # Initialize linked lists for each contour
    contour_heads = []
    active_nodes = []
    
    for contour in contours:
        if len(contour) < 2:
            contour_heads.append(None)
            continue
            
        node = Node(contour)
        node.fit()
        contour_heads.append(node)
        if node.curve:
            active_nodes.append(node)
            total_curves += 1
            
    # Heapify active nodes based on error
    # heapq stores tuples. We want max error.
    heap = []
    import itertools
    counter = itertools.count() # Unique tie-breaker
    
    for node in active_nodes:
        # We only split if we can (len > 3 usually, or error > threshold)
        if len(node.points) >= 4:
            heapq.heappush(heap, (-node.error, next(counter), node))
            
    while total_curves < target_count and heap:
        neg_err, _, node = heapq.heappop(heap)
        
        # Split this node
        points = node.points
        curve = node.curve
        
        # Find split index
        u = chord_length_parameterize(points)
        max_dist = 0.0
        split_idx = len(points) // 2
        
        for i in range(len(points)):
            p_curve = cubic_bezier(u[i], curve[0], curve[1], curve[2], curve[3])
            dist = points[i].dist(p_curve)
            if dist > max_dist:
                max_dist = dist
                split_idx = i
        
        if split_idx == 0: split_idx = 1
        if split_idx == len(points) - 1: split_idx = len(points) - 2
        
        left_points = points[:split_idx+1]
        right_points = points[split_idx:]
        
        # Create new nodes
        left_node = Node(left_points)
        right_node = Node(right_points)
        
        left_node.fit()
        right_node.fit()
        
        # Update links
        # node.prev -> left -> right -> node.next
        left_node.prev = node.prev
        left_node.next = right_node
        right_node.prev = left_node
        right_node.next = node.next
        
        if node.prev:
            node.prev.next = left_node
        
        if node.next:
            node.next.prev = right_node
            
        # If node was head, update head
        # We need to find which contour this node belongs to.
        # This is expensive to search. 
        # Better: Node knows its contour index? Or just don't update heads yet.
        # We can just traverse from head? No, head might change.
        # Let's store 'is_head' or similar?
        # Actually, we can just store the list of nodes for each contour and replace?
        # Linked list is good for O(1) insertion/deletion.
        # We need to update the head pointer if we replaced the head.
        
        # Let's add a 'contour_idx' to Node
        # But wait, we don't strictly need to update contour_heads if we just collect results at the end.
        # We can collect results by traversing the linked list.
        # But we need to know where the list starts.
        # If we replace the head, the old head object is gone from the list.
        # So we DO need to update contour_heads[contour_idx].
        
        # Let's add contour_idx to Node
        pass # Logic handled below
        
        # Update total curves: -1 (removed parent) + 2 (added children) = +1
        total_curves += 1
        
        # Push children to heap
        if left_node.curve and len(left_node.points) >= 4:
            heapq.heappush(heap, (-left_node.error, next(counter), left_node))
        if right_node.curve and len(right_node.points) >= 4:
            heapq.heappush(heap, (-right_node.error, next(counter), right_node))
            
        # We need to handle the head update.
        # Since we don't have back-pointers to the list container, 
        # let's just use a wrapper or be careful.
        # Hack: We can keep the original 'head' node as a dummy or sentinel?
        # Or just update the list in `contour_heads`?
        # We don't have contour_idx in the loop.
        # Let's restart the structure with contour_idx.
        
    # Re-implementation with contour_idx tracking
    return _fit_curves_with_heap(contours, target_count)

def _fit_curves_with_heap(contours, target_count):
    import heapq
    import itertools
    
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
                
    while total_curves < target_count and heap:
        neg_err, _, node = heapq.heappop(heap)
        
        # Check if this node is still valid (it might have been processed? No, we pop and split)
        # But wait, if we have duplicate entries? No, we only push once.
        
        points = node.points
        curve = node.curve
        
        # Split logic
        u = chord_length_parameterize(points)
        max_dist = 0.0
        split_idx = len(points) // 2
        
        for i in range(len(points)):
            p_curve = cubic_bezier(u[i], curve[0], curve[1], curve[2], curve[3])
            dist = points[i].dist(p_curve)
            if dist > max_dist:
                max_dist = dist
                split_idx = i
        
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
