from typing import Tuple


class Coord:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Initializes a coordinate with x and y values."""
        self.x = x
        self.y = y

    def as_tuple(self) -> Tuple[float, float]:
        """Returns the coordinates as a tuple."""
        return self.x, self.y

    def __repr__(self):
        return f"Coord(x={self.x}, y={self.y})"
    
