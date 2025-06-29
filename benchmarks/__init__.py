from .compound_index_benchmark import CompoundIndexBenchmark
from .intersect_benchmark import IntersectBenchmark
from .no_index_benchmark import NoIndexBenchmark
from .single_index_benchmark import SingleIndexBenchmark

benchmark_list = [CompoundIndexBenchmark, IntersectBenchmark, NoIndexBenchmark, SingleIndexBenchmark]