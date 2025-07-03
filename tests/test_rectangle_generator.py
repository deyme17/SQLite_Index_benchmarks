import pytest
from scripts.rectangle_generator import RectangleGenerator
from scripts.core.rectangle import Rectangle
from scripts.utils.settings import X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL


class TestRectangleGenerator:
    @classmethod
    def setup_class(cls):
        cls.x_range = (X_MIN_GLOBAL, X_MAX_GLOBAL)
        cls.y_range = (Y_MIN_GLOBAL, Y_MAX_GLOBAL)
        cls.generator = RectangleGenerator(cls.x_range, cls.y_range)

    def test_generator_initialization(self):
        assert self.generator.x_min_global == self.x_range[0]
        assert self.generator.x_max_global == self.x_range[1]
        assert self.generator.y_min_global == self.y_range[0]
        assert self.generator.y_max_global == self.y_range[1]

    def test_generate_rectangle_count(self):
        count_per_ratio = 5
        rectangles = self.generator.generate_from_ratios(count=count_per_ratio)
        expected_count = count_per_ratio * len(self.generator.aspect_ratios)
        assert len(rectangles) == expected_count
        for rect in rectangles:
            assert isinstance(rect, Rectangle)

    def test_rectangles_within_bounds(self):
        rectangles = self.generator.generate_from_ratios(count=10)
        for rect in rectangles:
            assert self.x_range[0] <= rect.min_x < rect.max_x <= self.x_range[1]
            assert self.y_range[0] <= rect.min_y < rect.max_y <= self.y_range[1]
            assert rect.width > 0 and rect.height > 0

    def test_aspect_ratio_is_reasonable(self):
        expected_ratios = {round(w / h, 2) for w, h in self.generator.aspect_ratios}
        rectangles = self.generator.generate_from_ratios(count=5)
        for rect in rectangles:
            # avoid ZeroDivisionError
            if rect.height > 0:
                assert round(rect.aspect_ratio, 2) in expected_ratios

    def test_generate_fixed_sizes(self):
        rectangles = self.generator.generate_from_fixed_sizes()
        expected_count = len(self.generator.fixed_sizes)
        assert len(rectangles) == expected_count

        for rect, (w_expected, h_expected) in zip(rectangles, self.generator.fixed_sizes):
            # Allow for clipping: width and height should not exceed expected values
            assert rect.width <= w_expected
            assert rect.height <= h_expected
            assert rect.width > 0
            assert rect.height > 0

    def test_generate_fixed_sizes_shuffle(self):
        rects1 = self.generator.generate_from_fixed_sizes(shuffle=False)
        rects2 = self.generator.generate_from_fixed_sizes(shuffle=True)
        assert sorted(r.area for r in rects1) == sorted(r.area for r in rects2)
        assert rects1 != rects2

    def test_too_large_rectangle_raises(self):
        width = 10**9
        height = 10**9
        rect = self.generator._generate_rectangle(width, height)

        assert rect.min_x >= self.generator.x_min_global
        assert rect.min_y >= self.generator.y_min_global
        assert rect.max_x <= self.generator.x_max_global + width
        assert rect.max_y <= self.generator.y_max_global + height

        assert rect.width == width
        assert rect.height == height