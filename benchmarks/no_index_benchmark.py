from benchmarks.benchmark_interface import BenchmarkInterface

class NoIndexBenchmark(BenchmarkInterface):
    @classmethod
    def get_benchmark_name(cls) -> str:
        """Returns unique benchmark identifier."""
        return 'no_index'
    
    def _get_db_path(self) -> str:
        return "db/no_index.db"
    
    def perform_benchmark(self, x_min: float, x_max: float, y_min: float, y_max: float, repeat: int = 5, aggregate: bool = False) -> dict:
        """Executes standard bounding box query on database with no indecies."""
        return self.runner.run_default_query(x_min, x_max, y_min, y_max, repeat, aggregate)