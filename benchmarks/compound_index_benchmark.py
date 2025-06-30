from benchmarks.benchmark_interface import BenchmarkInterface

class CompoundIndexBenchmark(BenchmarkInterface):
    @classmethod
    def get_benchmark_name(cls) -> str:
        """Returns unique benchmark identifier."""
        return 'compound_index_benchmark'
    
    def _get_db_path(self) -> str:
        return "db/compound_index.db"
    
    def perform_benchmark(self, x_min: float, x_max: float, y_min: float, y_max: float, repeat: int = 1) -> dict:
        """Executes standard bounding box query on compound-indexed database."""
        return self.runner.run_default_query(x_min, x_max, y_min, y_max, repeat)