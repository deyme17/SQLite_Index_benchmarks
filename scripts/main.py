from scripts.benchmark_runner import BenchmarkRunner
from scripts.coord_generator import CoordGenerator
from scripts.results_saver import ResultsSaver

if __name__ == "__main__":
    runner = BenchmarkRunner("db/KievRegion.db")
    coords = CoordGenerator((800000, 950000), (5500000, 5800000), rect_size=10000)
    saver = ResultsSaver()

    for rect in coords.generate(n=10):
        result = runner.run_query(*rect, limit=500)
        saver.add_result(result)

    saver.save()
