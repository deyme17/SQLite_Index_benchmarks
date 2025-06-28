import sqlite3

def get_total_records(db_path):
    """
    Returns the total records (count) from the 'sgmstr' table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sgmstr")
    count = cursor.fetchone()[0]

    conn.close()

    if count:
        return count
    else:
        raise ValueError("Could not determine total records from database.")
    
if __name__ == "__main__":
    print(get_total_records("db/KievRegion.db"))