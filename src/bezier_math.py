import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"
    
    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def bernstein_poly(n, i, t):
    """
    Calculates the Bernstein polynomial B_{i,n}(t).
    B_{i,n}(t) = C(n, i) * t^i * (1-t)^(n-i)
    """
    if i < 0 or i > n:
        return 0
    binomial_coeff = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
    return binomial_coeff * (t ** i) * ((1 - t) ** (n - i))

def cubic_bezier(t, p0, p1, p2, p3):
    """
    Evaluates a cubic Bezier curve at parameter t.
    Returns a Point.
    """
    # B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3
    # Using Bernstein polynomials:
    # B(t) = B_{0,3}(t)P0 + B_{1,3}(t)P1 + B_{2,3}(t)P2 + B_{3,3}(t)P3
    
    b0 = bernstein_poly(3, 0, t)
    b1 = bernstein_poly(3, 1, t)
    b2 = bernstein_poly(3, 2, t)
    b3 = bernstein_poly(3, 3, t)
    
    return p0 * b0 + p1 * b1 + p2 * b2 + p3 * b3

def evaluate_curve_length(p0, p1, p2, p3, steps=100):
    """
    Estimates the length of the cubic Bezier curve using numerical integration (chord summation).
    """
    length = 0.0
    prev_point = p0
    for i in range(1, steps + 1):
        t = i / steps
        curr_point = cubic_bezier(t, p0, p1, p2, p3)
        length += prev_point.dist(curr_point)
        prev_point = curr_point
    return length
