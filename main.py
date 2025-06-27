from scripts.benchmark_runner import BenchmarkRunner
from scripts.rectangle_generator import RectangleGenerator
from scripts.results_saver import ResultsSaver

if __name__ == "__main__":
    runner = BenchmarkRunner("db/KievRegion.db")
    generator = RectangleGenerator((40, 800000), (30, 600000))
    saver = ResultsSaver()

    for rect in generator.generate_rectangles(count=100, min_size=1000, max_size=50000):
        try:
            result = runner.run_query(*rect.to_bounds(), limit=500)
            saver.add_result(result)
        except Exception as e:
            print(f"Error processing rectangle {rect}: {e}")

    saver.save()