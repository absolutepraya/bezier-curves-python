import cv2
import numpy as np
from bezier_math import Point

def get_contours(image_path, min_area=100):
    """
    Loads an image, processes it, and extracts contours.
    Returns a list of contours, where each contour is a list of Point objects.
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge Detection (Canny)
    edges = cv2.Canny(img, 100, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    processed_contours = []
    for cnt in contours:
        # Filter small noise
        if cv2.contourArea(cnt) < min_area:
            continue
        
        points = []
        for p in cnt:
            x, y = p[0]
            points.append(Point(float(x), float(y)))
        
        processed_contours.append(points)

    return processed_contours, img.shape
