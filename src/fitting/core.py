import sys
import os

# Add parent directory to path to allow importing bezier_math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bezier_math import Point, cubic_bezier

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
        return None 

    p0 = points[0]
    p3 = points[-1]

    if n == 2:
        # Straight line
        p1 = p0 * (2/3) + p3 * (1/3)
        p2 = p0 * (1/3) + p3 * (2/3)
        return [p0, p1, p2, p3]

    u = chord_length_parameterize(points)
    
    # Solve system of equations for Least Squares fitting
    c11 = 0.0
    c12 = 0.0
    c22 = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0

    # Accumulate terms for the system of equations
    for i in range(n):
        t = u[i]
        a1 = 3 * (1-t)**2 * t
        a2 = 3 * (1-t) * t**2
        
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

    det = c11 * c22 - c12 * c12
    
    if abs(det) < 1e-9:
        # Singular matrix, fallback to straight line
        p1 = p0 * (2/3) + p3 * (1/3)
        p2 = p0 * (1/3) + p3 * (2/3)
        return [p0, p1, p2, p3]

    # Inverse matrix multiplication
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
