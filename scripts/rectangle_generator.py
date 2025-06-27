import random as rnd
from typing import List, Tuple
from scripts.core.rectangle import Rectangle
from scripts.core.coord import Coord


class RectangleGenerator:
    def __init__(self, x_range: Tuple[int, int], y_range: Tuple[int, int]):
        self.x_min_global, self.x_max_global = x_range
        self.y_min_global, self.y_max_global = y_range

        self.aspect_ratios: List[Tuple[int, int]] = [
            (4, 3), (16, 9), (1, 1), (2, 1), (3, 2), (5, 4),
            (21, 9), (1, 2), (3, 4), (9, 16), (9, 12), (5, 3)
        ]

        self.fixed_sizes: List[Tuple[int, int]] = [
            (40, 30), (80, 60), (160, 120), (200, 150),
            (400, 300), (800, 600), (1600, 1200), (2000, 1500),
            (4000, 3000), (8000, 6000), (16000, 12000), (20000, 15000),
            (40000, 30000), (80000, 60000), (160000, 120000),
            (200000, 150000), (400000, 300000), (800000, 600000)
        ]

    def generate_rectangles(self, count: int = 10, min_size: int = 1000, max_size: int = 50000) -> List[Rectangle]:
        """Generates a list of Rectangle objects with valid random bounds."""
        rectangles = []

        for _ in range(count):
            x_aspect, y_aspect = rnd.choice(self.aspect_ratios)
            width = rnd.randint(min_size, max_size)
            height = int(width * y_aspect / x_aspect)

            rectangle = self._generate_rectangle(width, height)
            if rectangle is None:
                continue
            
            rectangles.append(rectangle)

        return rectangles

    def generate_from_fixed_sizes(self, shuffle: bool = False) -> List[Rectangle]:
        """Generates rectangles with fixed sizes."""
        sizes = self.fixed_sizes[:]
        if shuffle:
            rnd.shuffle(sizes)

        rectangles = []
        for width, height in sizes:
            rectangle = self._generate_rectangle(width, height)
            if rectangle is None:
                continue

            rectangles.append(rectangle)

        return rectangles

    def _generate_rectangle(self, width: int, height: int) -> Rectangle|None:
        """Generates a single rectangle with specified width and height."""
        max_x_start = self.x_max_global - width
        max_y_start = self.y_max_global - height

        if max_x_start < self.x_min_global or max_y_start < self.y_min_global:
            print("Rectangle size exceeds global bounds. It was clipped to valid range.")
            max_x_start = self.x_min_global
            max_y_start = self.y_min_global

        x_start = rnd.randint(self.x_min_global, max_x_start)
        y_start = rnd.randint(self.y_min_global, max_y_start)

        min_coord = Coord(x_start, y_start)
        max_coord = Coord(x_start + width, y_start + height)

        return Rectangle(min_coord, max_coord)
