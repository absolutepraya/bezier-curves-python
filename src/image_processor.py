import cv2
import numpy as np
from bezier_math import Point

def get_contours(image_path, min_area=100):
    """
    Loads an image, processes it, and extracts contours.
    Returns a list of contours, where each contour is a list of Point objects.
    """
    # 1. Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # 2. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Edge Detection (Canny)
    # Canny is more robust for finding edges regardless of brightness direction.
    # We use standard thresholds 100 and 200.
    edges = cv2.Canny(img, 100, 200)

    # 4. Find contours
    # RETR_EXTERNAL retrieves only the extreme outer contours. 
    # RETR_LIST retrieves all contours.
    # CHAIN_APPROX_NONE stores all the contour points (no approximation).
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    processed_contours = []
    for cnt in contours:
        # Filter small noise
        if cv2.contourArea(cnt) < min_area:
            continue
        
        # Convert numpy array (N, 1, 2) to list of Points
        # Note: cv2 points are (x, y), and image coordinates have y growing downwards.
        # We keep this coordinate system for now (PDF also has y, but usually growing upwards, 
        # we might need to flip y later or in the PDF generator).
        points = []
        for p in cnt:
            x, y = p[0]
            points.append(Point(float(x), float(y)))
        
        processed_contours.append(points)

    return processed_contours, img.shape
