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
