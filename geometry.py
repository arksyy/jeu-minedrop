"""Helpers geometriques pour les landmarks de pose."""
import math
from typing import Tuple

Point = Tuple[float, float]


def distance(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_deg(a: Point, b: Point, c: Point) -> float:
    """Angle (degres) au sommet b, forme par les segments b->a et b->c."""
    ax, ay = a[0] - b[0], a[1] - b[1]
    cx, cy = c[0] - b[0], c[1] - b[1]
    dot = ax * cx + ay * cy
    mag = math.hypot(ax, ay) * math.hypot(cx, cy)
    if mag < 1e-9:
        return 0.0
    cos_theta = max(-1.0, min(1.0, dot / mag))
    return math.degrees(math.acos(cos_theta))
