from .core import fit_cubic_bezier, calculate_max_error, chord_length_parameterize
from bezier_math import cubic_bezier

def fit_curve_recursive(points, error_threshold=2.0):
    """
    Recursively fits Bezier curves to the points.
    If the error is too large, splits the points and fits again.
    """

    # If less than 2 points, cannot form any curve
    if len(points) < 2:
        return []
    
    # Fit a cubic Bezier curve to the points
    curve = fit_cubic_bezier(points)
    if curve is None:
        return []

    max_err = calculate_max_error(points, curve)
    
    # If error is within threshold or not enough points to split further, return the curve
    if max_err < error_threshold or len(points) < 4:
        return [curve]
    
    # Split points at the point of maximum error
    # To find the split index, we re-evaluate distances
    u = chord_length_parameterize(points)
    max_dist = 0.0
    split_idx = len(points) // 2 # Default split
    
    # Find the point with maximum error
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
