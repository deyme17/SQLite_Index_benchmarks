from scripts.benchmark_runner import BenchmarkRunner
from scripts.rectangle_generator import RectangleGenerator
from scripts.results_saver import ResultsSaver
from benchmarks import benchmark_list
from scripts.utils.settings import X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL

import sys
import getopt


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

        suffix = "_det" if detailed else "_agg" # _det - detailed; _agg - aggregated
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
    detailed = False
    repeat = 20
    
    # parse args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dhr:", ["detailed", "help", "repeat="])
    except getopt.GetoptError as err:
        print(f"Error: {err}")
        print("Use --help for usage hint")
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ("-d", "--detailed"):
            detailed = True

        elif opt in ("-r", "--repeat"):
            try:
                repeat = int(arg)
            except ValueError:
                print(f"Error: Invalid repeat value '{arg}'. Must be an integer.")
                sys.exit(1)
                
        elif opt in ("-h", "--help"):
            print("Usage: python main.py [args]")
            print("args:")
            print("  -d, --detailed     Enable detailed mode")
            print("  -r, --repeat N     Set number of repetitions (default: 20)")
            print("  -h, --help         Show this help message")
            sys.exit(0)

    run_benchmarks(benchmark_list=benchmark_list, detailed=detailed, repeat=20)