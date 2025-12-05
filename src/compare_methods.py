import cv2
import numpy as np
from bezier_math import Point
from curve_fitter import fit_curve_recursive
from pdf_generator import generate_pdf_from_curves

def get_contours(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    point_contours = []
    for cnt in contours:
        points = []
        for p in cnt:
            points.append(Point(float(p[0][0]), float(p[0][1])))
        if len(points) > 1:
            point_contours.append(points)
            
    return point_contours, (img.shape[0], img.shape[1])

def pure_interpolation(points):
    """
    Naively fits Bezier curves by taking every 4th point.
    This is a simplified "Pure Interpolation" where we force the curve to pass through specific points.
    For a true interpolation of N points, we'd need to solve a system of equations, 
    but for comparison, "sampling" is a good proxy for "high density curves".
    """
    curves = []
    
    for i in range(len(points) - 1):
        p0 = points[i]
        p3 = points[i+1]
        # Straight line approximation for "connecting the dots"
        p1 = Point(p0.x * (2/3) + p3.x * (1/3), p0.y * (2/3) + p3.y * (1/3))
        p2 = Point(p0.x * (1/3) + p3.x * (2/3), p0.y * (1/3) + p3.y * (2/3))
        curves.append([p0, p1, p2, p3])
        
    return curves

def main():
    input_path = "input/makara.png" # Hardcoded for demo
    print(f"Comparing methods on {input_path}...")
    
    contours, dims = get_contours(input_path)
    if not contours:
        print("Failed to load image.")
        return

    height, width = dims
    
    # Hybrid (Least Squares)
    print("\n--- Method 1: Hybrid (Least Squares) ---")
    hybrid_curves = []
    for contour in contours:
        hybrid_curves.extend(fit_curve_recursive(contour, error_threshold=2.0))
    
    print(f"Total Curves: {len(hybrid_curves)}")
    generate_pdf_from_curves([hybrid_curves], "output/comparison_hybrid.pdf", width, height)
    print("Saved to output/comparison_hybrid.pdf")

    # Pure Interpolation (Connect every point)
    print("\n--- Method 2: Pure Interpolation (Connect Dots) ---")
    pure_curves = []
    for contour in contours:
        pure_curves.extend(pure_interpolation(contour))
        
    print(f"Total Curves: {len(pure_curves)}")
    generate_pdf_from_curves([pure_curves], "output/comparison_pure.pdf", width, height)
    print("Saved to output/comparison_pure.pdf")
    
    print("\nComparison:")
    print(f"Hybrid Count: {len(hybrid_curves)}")
    print(f"Pure Count  : {len(pure_curves)}")
    print(f"Efficiency  : Hybrid uses {len(hybrid_curves)/len(pure_curves)*100:.2f}% of the curves used by Pure Interpolation.")

if __name__ == "__main__":
    main()
