from benchmarks.benchmark_interface import BenchmarkInterface

class IntersectBenchmark(BenchmarkInterface):
    @classmethod
    def get_benchmark_name(cls) -> str:
        """Returns unique benchmark identifier."""
        return 'intersect'
    
    def _get_db_path(self) -> str:
        return "db/double_index.db"
    
    def perform_benchmark(self, x_min: float, x_max: float, y_min: float, y_max: float, repeat: int = 1) -> dict:
        """Executes an INTERSECT bounding box query on database with double index."""
        return self.runner.run_intersect_query(x_min, x_max, y_min, y_max, repeat)