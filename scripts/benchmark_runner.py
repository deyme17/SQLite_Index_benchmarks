import sqlite3 as sql
import time


class BenchmarkRunner:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def run_query(self, x_min: float, x_max: float, y_min: float, y_max: float, limit: int = 1000) -> dict:
        query = """
            SELECT * FROM sgmstr 
            WHERE x > ? AND x < ? 
              AND y > ? AND y < ?
            LIMIT ?
        """
        params = [x_min, x_max, y_min, y_max, limit]
        return self._execute_benchmark(query, params, "basic", x_min, x_max, y_min, y_max, limit)

    def run_intersect_query(self, x_min: float, x_max: float, y_min: float, y_max: float, limit: int = 1000) -> dict:
        query = """
            SELECT * FROM (
                SELECT * FROM sgmstr WHERE x > ? AND x < ?
                INTERSECT
                SELECT * FROM sgmstr WHERE y > ? AND y < ?
            )
            LIMIT ?
        """
        params = [x_min, x_max, y_min, y_max, limit]
        return self._execute_benchmark(query, params, "intersect", x_min, x_max, y_min, y_max, limit)

    def _execute_benchmark(self, 
                           query: str, 
                           params: list, 
                           mode: str,
                           x_min: float, x_max: float, 
                           y_min: float, y_max: float,
                           limit: int) -> dict:
        """
        Executes a given query with timing and returns benchmark results.
        """
        conn, cursor = self._connect()

        start = time.perf_counter()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        duration = time.perf_counter() - start

        self._close_connection(conn)

        return {
            "mode": mode,
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max,
            "limit": limit,
            "row_count": len(rows),
            "execution_time_ms": round(duration * 1000, 3)
        }

    def _connect(self):
        """Connects to the SQLite database and returns connection and cursor."""
        conn = sql.connect(self.db_path)
        return conn, conn.cursor()

    def _close_connection(self, conn):
        """Closes the database connection."""
        if conn:
            conn.close()