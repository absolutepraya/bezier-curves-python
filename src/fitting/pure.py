import sys
import os

# Add parent directory to path to allow importing bezier_math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bezier_math import Point

def fit_curve_pure_interpolation(points):
    """
    Naively fits Bezier curves by connecting every consecutive point with a straight line.
    This represents "Pure Interpolation" where the curve must pass through every point.
    """
    curves = []
    
    if len(points) < 2:
        return []
        
    for i in range(len(points) - 1):
        p0 = points[i]
        p3 = points[i+1]
        
        # Straight line approximation: P1 = 2/3 P0 + 1/3 P3, P2 = 1/3 P0 + 2/3 P3
        p1 = Point(p0.x * (2/3) + p3.x * (1/3), p0.y * (2/3) + p3.y * (1/3))
        p2 = Point(p0.x * (1/3) + p3.x * (2/3), p0.y * (1/3) + p3.y * (2/3))
        
        curves.append([p0, p1, p2, p3])
        
    return curves
