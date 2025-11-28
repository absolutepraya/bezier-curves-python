import cv2
import numpy as np
from bezier_math import cubic_bezier

def generate_png_from_curves(curves, output_filename, width, height, line_color=(0, 0, 0), thickness=2):
    """
    Generates a PNG image from a list of Bezier curves.
    
    Args:
        curves: List of lists of curves. Each curve is [p0, p1, p2, p3].
        output_filename: Path to save the PNG file.
        width: Width of the image.
        height: Height of the image.
        line_color: Color of the curves (B, G, R). Default is black.
        thickness: Thickness of the curves.
    """
    # Create a white background
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    for contour_curves in curves:
        if not contour_curves:
            continue
            
        for curve in contour_curves:
            p0, p1, p2, p3 = curve
            
            # Evaluate points along the curve
            # 20 steps is usually enough for a smooth look at normal resolutions
            steps = 20 
            points = []
            for i in range(steps + 1):
                t = i / steps
                pt = cubic_bezier(t, p0, p1, p2, p3)
                # Ensure coordinates are integers for cv2
                points.append([int(pt.x), int(pt.y)])
            
            # Draw the curve segment
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], False, line_color, thickness, lineType=cv2.LINE_AA)
            
    cv2.imwrite(output_filename, image)
