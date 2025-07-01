from benchmarks.benchmark_interface import BenchmarkInterface

class XIndexBenchmark(BenchmarkInterface):
    @classmethod
    def get_benchmark_name(cls) -> str:
        """Returns unique benchmark identifier."""
        return 'x_index'
    
    def _get_db_path(self) -> str:
        return "db/single_index_x.db"
    
    def perform_benchmark(self, x_min: float, x_max: float, y_min: float, y_max: float, repeat: int = 5, aggregate: bool = False) -> dict:
        """Executes standard bounding box query on X-indexed database."""
        return self.runner.run_default_query(x_min, x_max, y_min, y_max, repeat, aggregate)