import sqlite3 as sql
import shutil
from pathlib import Path

from scripts.utils.settings import ORIGINAL_DB

OUTPUT_DIR = Path("db")
OUTPUT_DIR.mkdir(exist_ok=True)

VARIANTS = {
    "no_index.db": [],
    
    "single_index_x.db": [
        "CREATE INDEX IF NOT EXISTS idx_x ON SGMSTR(x);"
    ],
    
    "single_index_y.db": [
        "CREATE INDEX IF NOT EXISTS idx_y ON SGMSTR(y);"
    ],
    
    "double_index.db": [
        "CREATE INDEX IF NOT EXISTS idx_x ON SGMSTR(x);",
        "CREATE INDEX IF NOT EXISTS idx_y ON SGMSTR(y);"
    ],
    
    "compound_index.db": [
        "CREATE INDEX IF NOT EXISTS idx_x_y ON SGMSTR(x, y);"
    ]
}

def create_variant_db(variant_name: str, index_statements: list[str]):
    target_path = OUTPUT_DIR / variant_name
    shutil.copy(ORIGINAL_DB, target_path)

    conn = sql.connect(target_path)
    cursor = conn.cursor()

    cursor.executescript("""
        DROP INDEX IF EXISTS idx_lat;
        DROP INDEX IF EXISTS idx_lon;
        DROP INDEX IF EXISTS idx_lat_lon;
    """)

    for stmt in index_statements:
        cursor.execute(stmt)

    conn.commit()
    conn.close()
    print(f"Created {variant_name}")


if __name__ == "__main__":
    for name, indexes in VARIANTS.items():
        create_variant_db(name, indexes)
