import os
import csv
from typing import List

class ResultsSaver:
    def __init__(self, path: str = "results/benchmark_results.csv"):
        self.path = path
        self.results: List[dict] = []
        # make dir if not exists
        os.makedirs(name=os.path.dirname(self.path), exist_ok=True)

    def add_result(self, result: dict):
        """Just append the benchmark result to the buffer of collected results."""
        self.results.append(result)

    def save_as_csv(self):
        """Saves all collected results in CSV-file."""
        if not self.results:
            print("No results to save.")
            return
        
        columns = list(self.results[0].keys())
        is_empty = not os.path.isfile(self.path) or os.stat(self.path).st_size == 0
        
        with open(self.path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, columns)

            if not is_empty:
                writer.writeheader()
            
            writer.writerows(self.results)

        print(f"Saved {len(self.results)} results to {self.path}.")
        self.results.clear()