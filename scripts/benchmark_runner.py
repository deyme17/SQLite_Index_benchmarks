import sqlite3 as sql
import time


class BenchmarkRunner:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def run_default_query(self, x_min: float, x_max: float, y_min: float, y_max: float,
                          repeat: int = 1, aggregate: bool = False) -> dict | list[dict]:
        """Run a basic SELECT query with bounding box filtering on x and y columns."""
        query = """
            SELECT * FROM sgmstr 
            WHERE x > ? AND x < ? 
              AND y > ? AND y < ?
        """
        params = [x_min, x_max, y_min, y_max]
        return self._run_query_with_mode(query, params, x_min, x_max, y_min, y_max, repeat, aggregate)

    def run_intersect_query(self, x_min: float, x_max: float, y_min: float, y_max: float,
                            repeat: int = 1, aggregate: bool = False) -> dict | list[dict]:
        """Run a SELECT query using INTERSECT between x and y filters."""
        query = """
            SELECT * FROM sgmstr WHERE x > ? AND x < ?
            INTERSECT
            SELECT * FROM sgmstr WHERE y > ? AND y < ?
        """
        params = [x_min, x_max, y_min, y_max]
        return self._run_query_with_mode(query, params, x_min, x_max, y_min, y_max, repeat, aggregate)

    def run_custom_query(self, query: str, params: list,
                         x_min: float, x_max: float, y_min: float, y_max: float,
                         repeat: int = 1, aggregate: bool = False) -> dict | list[dict]:
        """Run a custom SQL query with given parameters and bounding box metadata."""
        return self._run_query_with_mode(query, params, x_min, x_max, y_min, y_max, repeat, aggregate)

    def _run_query_with_mode(self, query: str, params: list,
                             x_min: float, x_max: float, y_min: float, y_max: float,
                             repeat: int, aggregate: bool) -> dict | list[dict]:
        """Helper method to execute query with or without aggregation."""
        if aggregate:
            return self._execute_aggregated_benchmark(query, params, x_min, x_max, y_min, y_max, repeat)
        else:
            return self._execute_benchmark(query, params, x_min, x_max, y_min, y_max, repeat)

    def _execute_aggregated_benchmark(self, query: str, params: list,
                                      x_min: float, x_max: float, y_min: float, y_max: float,
                                      repeat: int) -> dict:
        """
        Executes a given query with timing (multiple times) and returns aggregated benchmark results.
        """
        total_rows = 0
        total_time = 0.0

        for _ in range(repeat):
            conn, cursor = self._connect()
            cursor.execute("PRAGMA shrink_memory;")  # to disable cache

            start = time.perf_counter()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            duration = time.perf_counter() - start

            total_rows += len(rows)
            total_time += duration

            self._close_connection(conn)

        return {
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max,
            "repeat": repeat,
            "row_count_total": total_rows,
            "row_count_avg": total_rows // repeat,
            "execution_time_total_ms": round(total_time * 1000, 3),
            "execution_time_avg_ms": round((total_time / repeat) * 1000, 3),
        }

    def _execute_benchmark(self, query: str, params: list,
                           x_min: float, x_max: float, y_min: float, y_max: float,
                           repeat: int) -> list[dict]:
        """
        Executes a given query with timing (multiple times) and returns individual benchmark results.
        """
        results = []

        for _ in range(repeat):
            conn, cursor = self._connect()
            cursor.execute("PRAGMA shrink_memory;")  # to disable cache

            start = time.perf_counter()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            duration = time.perf_counter() - start

            self._close_connection(conn)

            results.append({
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "records_count": len(rows),
                "execution_time_ms": round(duration * 1000, 3),
            })

        return results

    def _connect(self):
        """Connects to the SQLite database and returns connection and cursor."""
        conn = sql.connect(self.db_path)
        return conn, conn.cursor()

    def _close_connection(self, conn):
        """Closes the database connection."""
        if conn:
            conn.close()