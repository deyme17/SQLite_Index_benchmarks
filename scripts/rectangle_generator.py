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

    def generate_rectangles_from_ratios(self, ratios: List[Tuple[int, int]] = None, count: int = 1, min_size: int = 1000, max_size: int = 50000) -> List[Rectangle]:
        """
        Generates rectangles based on aspect ratios.
        Args:
            ratios: Optional list of (width_ratio, height_ratio) tuples.
                    If not provided, default aspect ratios will be used.
            count: Number of rectangles to generate for each ratio.
            min_size: Minimum width of the generated rectangles.
            max_size: Maximum width of the generated rectangles.
        Return: 
            List of generated Rectangle objects.
        """
        aspect_ratios = self.aspect_ratios if ratios is None else ratios
        rectangles = []

        for curr_ratio in aspect_ratios:
            for _ in range(count):
                x_aspect, y_aspect = curr_ratio
                if x_aspect == 0:
                    print(f"Invalid aspect ratio: ({x_aspect}, {y_aspect}), skipping.")
                    continue

                width = rnd.randint(min_size, max_size)
                height = int(width * y_aspect / x_aspect)

                rectangle = self._generate_rectangle(width, height)
                if rectangle is None:
                    continue
                
                rectangles.append(rectangle)

        return rectangles

    def generate_from_fixed_sizes(self, sizes: List[Tuple[int, int]] = None, shuffle: bool = False) -> List[Rectangle]:
        """
        Generates rectangles using fixed predefined sizes.
        Args:
            sizes: Optional list of (width, height) tuples. 
                   If not provided, default fixed sizes will be used.
            shuffle: If True, randomly shuffle the order of sizes before generation.
        Return:
            List of generated Rectangle objects.
        """
        sizes = self.fixed_sizes[:] if sizes is None else sizes
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
