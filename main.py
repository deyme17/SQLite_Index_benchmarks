from scripts.benchmark_runner import BenchmarkRunner
from scripts.rectangle_generator import RectangleGenerator
from scripts.results_saver import ResultsSaver
from scripts.utils.settings import X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL, ORIGINAL_DB

if __name__ == "__main__":
    runner = BenchmarkRunner(ORIGINAL_DB)
    generator = RectangleGenerator((X_MIN_GLOBAL, X_MAX_GLOBAL), (Y_MIN_GLOBAL, Y_MAX_GLOBAL))
    saver = ResultsSaver()

    for rect in generator.generate_rectangles(count=100, min_size=1000, max_size=50000):
        try:
            result = runner.run_query(*rect.to_bounds(), limit=500)
            saver.add_result(result)
        except Exception as e:
            print(f"Error processing rectangle {rect}: {e}")

    saver.save()