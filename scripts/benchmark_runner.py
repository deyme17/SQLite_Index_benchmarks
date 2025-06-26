import sqlite3 as sql
import time


class BenchmarkRunner:
    def __init__(self, db_path):
        self.db_path = db_path

    def run_query(self, x_min, x_max, y_min, y_max, limit=1000):
        """        
        Runs a benchmark query on the database.
        Args:
            x_min (float): Minimum x-coordinate.
            x_max (float): Maximum x-coordinate.
            y_min (float): Minimum y-coordinate.
            y_max (float): Maximum y-coordinate.
            limit (int): Maximum number of results to return.
        Returns:
            dict with execution time, row count, and query bounds.
        """
        conn, cursor = self._connect()

        query = """
            SELECT * FROM sgmstr 
            WHERE x > ? AND x < ? 
                AND y > ? AND y < ?
            LIMIT ?
        """

        # start the timer (use perf_counter for more precise timing)
        start = time.perf_counter()

        cursor.execute(query, (x_min, x_max, y_min, y_max, limit))
        rows = cursor.fetchall()

        # end the timer
        duration = time.perf_counter() - start

        self._close_connection(conn)

        return {
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max,
            "limit": limit,
            "row_count": len(rows),
            "execution_time": round(duration * 1000, 3)
        }

    def _connect(self):
        """Connects to the SQLite database and returns connection and cursor."""
        conn = sql.connect(self.db_path)
        return conn, conn.cursor()

    def _close_connection(self, conn):
        """Closes the database connection."""
        if conn:
            conn.close()