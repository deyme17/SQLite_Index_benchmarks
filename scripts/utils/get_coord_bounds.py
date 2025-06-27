import sqlite3

def get_coordinate_bounds(db_path: str) -> tuple[float, float, float, float]:
    """
    Returns the min and max values of x and y from the 'sgmstr' table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT MIN(x), MAX(x), MIN(y), MAX(y) FROM sgmstr")
    result = cursor.fetchone()

    conn.close()

    if result and all(r is not None for r in result):
        x_min, x_max, y_min, y_max = result
        return x_min, x_max, y_min, y_max
    else:
        raise ValueError("Could not determine coordinate bounds from database.")

if __name__ == "__main__":
    print(get_coordinate_bounds("db/KievRegion.db"))
    