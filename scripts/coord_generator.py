class CoordGenerator: # тут кароч надо генерировать случайные координаты для прямоугольников разных размеров но стандартных пропорций (штук 20)
    def __init__(self, x_range: tuple, y_range: tuple, rect_size: int):
        ...
    def generate(self, n: int) -> list[tuple]:
        """Returns list of (x_min, x_max, y_min, y_max)"""
