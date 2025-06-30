from scripts.benchmark_runner import BenchmarkRunner
from scripts.rectangle_generator import RectangleGenerator
from scripts.results_saver import ResultsSaver
from benchmarks import benchmark_list
from scripts.utils.settings import X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL

if __name__ == "__main__":
    generator = RectangleGenerator((X_MIN_GLOBAL, X_MAX_GLOBAL), (Y_MIN_GLOBAL, Y_MAX_GLOBAL))

    for benchmark in benchmark_list:
        benchmark_performer = benchmark(BenchmarkRunner)
        saver = ResultsSaver(path=f"results/{benchmark_performer.get_benchmark_name()}_result.csv")

        for rect in generator.generate_from_fixed_sizes():
            try:
                result = benchmark_performer.perform_benchmark(*rect.to_bounds(), repeat=20)
                saver.add_result(result)
            except Exception as e:
                print(f"Error processing rectangle {rect}: {e}")

        saver.save_as_csv()