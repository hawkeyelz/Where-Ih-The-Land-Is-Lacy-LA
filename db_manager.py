import sqlite3

DB_NAME = "lacy_la.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def load_case(case_id):
    """Fetches general metadata for a specific case."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def load_location(case_id, city_name):
    """Fetches details of a specific city within a case."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM locations WHERE case_id = ? AND city_name = ?", 
        (case_id, city_name)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def load_witnesses_for_location(case_id, city_name):
    """Fetches all witnesses/clues associated with a city."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM clues WHERE case_id = ? AND city_name = ?", 
        (case_id, city_name)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]