import sqlite3

def init_db():
    conn = sqlite3.connect("lacy_la.db")
    cursor = conn.cursor()

    # Create cases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        title TEXT,
        total_budget INTEGER,
        total_hours INTEGER
    )
    """)

    # Create locations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        case_id TEXT,
        city_name TEXT,
        country TEXT,
        description TEXT,
        PRIMARY KEY (case_id, city_name)
    )
    """)

    # Create clues table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clues (
        clue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT,
        city_name TEXT,
        witness_role TEXT,
        personality TEXT,
        clue_text TEXT,
        fake_clue_text TEXT,
        bribe_cost INTEGER DEFAULT 0,
        failed_text TEXT,
        is_locked BOOLEAN DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
    print("Database Schema initialized successfully!")

if __name__ == "__main__":
    init_db()