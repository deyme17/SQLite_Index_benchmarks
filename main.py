from scripts.benchmark_runner import BenchmarkRunner
from scripts.rectangle_generator import RectangleGenerator
from scripts.results_saver import ResultsSaver
from benchmarks import benchmark_list
from scripts.utils.settings import X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL


def run_benchmarks(benchmark_list, detailed=False, repeat=20):
    """
    Execute benchmarks with configurable output format.
    
    Args:
        benchmark_list (list): The list of benchmarks to perform.
        detailed (bool): If True, logs individual queries; if False, returns aggregated results
        repeat (int): Number of queries per window size (detailed) or repetitions per test (aggregated)
    """
    generator = RectangleGenerator((X_MIN_GLOBAL, X_MAX_GLOBAL), (Y_MIN_GLOBAL, Y_MAX_GLOBAL))

    for benchmark in benchmark_list:
        benchmark_performer = benchmark(BenchmarkRunner)

        suffix = "_det" if detailed else "_agg" # _dt - detailed; _agg - aggregated
        benchmark_name = benchmark_performer.get_benchmark_name()
        saver = ResultsSaver(path=f"results/{benchmark_name}{suffix}_res.csv")

        for rect in generator.generate_from_fixed_sizes():
            try:
                if detailed:
                    # Individual query logging
                    for _ in range(repeat):
                        result = benchmark_performer.perform_benchmark(*rect.to_bounds(), repeat=1)
                        saver.add_result(result)
                else:
                    # Aggregated results
                    result = benchmark_performer.perform_benchmark(*rect.to_bounds(), repeat=repeat)
                    saver.add_result(result)
            except Exception as e:
                print(f"Error processing rectangle {rect}: {e}")

        saver.save_as_csv()

# main section
if __name__ == "__main__":
    run_benchmarks(benchmark_list=benchmark_list, detailed=True, repeat=20)