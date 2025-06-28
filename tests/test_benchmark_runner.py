import pytest
import sqlite3 as sql
from scripts.benchmark_runner import BenchmarkRunner
from scripts.utils.settings import ORIGINAL_DB, X_MAX_GLOBAL, X_MIN_GLOBAL, Y_MAX_GLOBAL, Y_MIN_GLOBAL, TOTAL_RECORDS


class TestBenchmarkRunner:
    @classmethod
    def setup_class(cls):
        cls.db_path = ORIGINAL_DB
        cls.runner = BenchmarkRunner(cls.db_path)

        cls.x_min = X_MIN_GLOBAL
        cls.x_max = X_MAX_GLOBAL
        cls.y_min = Y_MIN_GLOBAL
        cls.y_max = Y_MAX_GLOBAL
        cls.total_records = TOTAL_RECORDS

    def test_runner_initialization(self):
        assert self.runner.db_path == self.db_path

    def test_database_accessible(self):
        conn, cursor = self.runner._connect()
        cursor.execute("SELECT COUNT(*) FROM sgmstr")
        count = cursor.fetchone()[0]
        assert count > 0
        self.runner._close_connection(conn)

    def test_connect_method(self):
        conn, cursor = self.runner._connect()
        assert isinstance(conn, sql.Connection)
        assert isinstance(cursor, sql.Cursor)

        cursor.execute("PRAGMA table_info(sgmstr)")
        columns = [row[1] for row in cursor.fetchall()]
        assert 'x' in columns
        assert 'y' in columns

        self.runner._close_connection(conn)

    def test_close_connection_method(self):
        conn, cursor = self.runner._connect()
        self.runner._close_connection(conn)

        with pytest.raises(sql.ProgrammingError):
            cursor.execute("SELECT 1")

    def test_close_connection_with_none(self):
        self.runner._close_connection(None)

    def test_run_query_basic(self):
        x_min = self.x_min + (self.x_max - self.x_min) * 0.1
        x_max = self.x_min + (self.x_max - self.x_min) * 0.2
        y_min = self.y_min + (self.y_max - self.y_min) * 0.1
        y_max = self.y_min + (self.y_max - self.y_min) * 0.2

        result = self.runner.run_query(x_min, x_max, y_min, y_max, repeat=1)

        assert isinstance(result, dict)
        assert result["x_min"] == x_min
        assert result["x_max"] == x_max
        assert result["y_min"] == y_min
        assert result["y_max"] == y_max
        assert result["repeat"] == 1
        assert "row_count_total" in result
        assert "row_count_avg" in result
        assert "execution_time_total_ms" in result
        assert "execution_time_avg_ms" in result
        assert isinstance(result["row_count_total"], int)
        assert isinstance(result["row_count_avg"], int)
        assert isinstance(result["execution_time_total_ms"], (int, float))
        assert isinstance(result["execution_time_avg_ms"], (int, float))
        assert result["execution_time_total_ms"] >= 0
        assert result["execution_time_avg_ms"] >= 0

    def test_run_query_multiple_repeats(self):
        x_min = self.x_min + (self.x_max - self.x_min) * 0.3
        x_max = self.x_min + (self.x_max - self.x_min) * 0.4
        y_min = self.y_min + (self.y_max - self.y_min) * 0.3
        y_max = self.y_min + (self.y_max - self.y_min) * 0.4

        repeat = 3
        result = self.runner.run_query(x_min, x_max, y_min, y_max, repeat=repeat)

        assert result["repeat"] == repeat
        assert result["row_count_total"] == result["row_count_avg"] * repeat
        assert result["execution_time_avg_ms"] <= result["execution_time_total_ms"]

    def test_run_intersect_query_basic(self):
        x_min = self.x_min + (self.x_max - self.x_min) * 0.2
        x_max = self.x_min + (self.x_max - self.x_min) * 0.8
        y_min = self.y_min + (self.y_max - self.y_min) * 0.2
        y_max = self.y_min + (self.y_max - self.y_min) * 0.8

        result = self.runner.run_intersect_query(x_min, x_max, y_min, y_max, repeat=1)
        assert isinstance(result, dict)
        assert result["repeat"] == 1

        normal_result = self.runner.run_query(x_min, x_max, y_min, y_max, repeat=1)
        assert result["row_count_total"] <= normal_result["row_count_total"]

    def test_run_query_empty_result(self):
        x_min = self.x_max + 1000
        x_max = self.x_max + 2000
        y_min = self.y_max + 1000
        y_max = self.y_max + 2000

        result = self.runner.run_query(x_min, x_max, y_min, y_max, repeat=1)
        assert result["row_count_total"] == 0
        assert result["row_count_avg"] == 0
        assert result["execution_time_total_ms"] >= 0

    def test_run_query_large_range(self):
        result = self.runner.run_query(
            self.x_min - 1, self.x_max + 1,
            self.y_min - 1, self.y_max + 1,
            repeat=1
        )
        assert result["row_count_total"] == self.total_records

    def test_invalid_database_path(self):
        invalid_runner = BenchmarkRunner("/nonexistent/path/db.sqlite")
        with pytest.raises(sql.OperationalError):
            invalid_runner.run_query(1.0, 2.0, 1.0, 2.0, repeat=1)

    def test_query_parameter_types(self):
        result_int = self.runner.run_query(1, 2, 1, 2, repeat=1)
        result_float = self.runner.run_query(1.0, 2.0, 1.0, 2.0, repeat=1)
        assert isinstance(result_int, dict)
        assert isinstance(result_float, dict)
        assert result_int["x_min"] == result_float["x_min"]
