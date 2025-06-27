from scripts.core.coord import Coord
from typing import Tuple


class Rectangle:
    def __init__(self, minCoord: Coord, maxCoord: Coord):
        """Initializes a rectangle with minimum and maximum coordinates."""
        self.min_x = minCoord.x
        self.min_y = minCoord.y
        self.max_x = maxCoord.x
        self.max_y = maxCoord.y

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    def to_bounds(self) -> Tuple[float, float, float, float]:
        """Returns the rectangle bounds as (x_min, x_max, y_min, y_max)."""
        return self.min_x, self.max_x, self.min_y, self.max_y

    def __repr__(self):
        return f"Rectangle(minCoord=({self.min_x, self.min_y}), maxCoord=({self.max_x, self.max_y}))"