from abc import ABC, abstractmethod

class BenchmarkInterface(ABC):
    def __init__(self, runner_class):
        self.runner = runner_class(self._get_db_path())

    @classmethod
    @abstractmethod
    def get_benchmark_name() -> str:
        pass

    @abstractmethod
    def _get_db_path(self) -> str:
        pass
    
    @abstractmethod
    def perform_benchmark(self, x_min, x_max, y_min, y_max, repeat=5, aggregate=False):
        pass