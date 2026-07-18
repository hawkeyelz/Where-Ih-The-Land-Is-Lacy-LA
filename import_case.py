import sqlite3
import json

def import_case_data():
    # Read our newly renamed JSON asset file
    with open("case_001.json", "r") as f:
        data = json.load(f)
        
    conn = sqlite3.connect("lacy_la.db")
    cursor = conn.cursor()
    
    # 1. Insert Case Meta
    cursor.execute("""
        INSERT OR REPLACE INTO cases (case_id, title, total_budget, total_hours)
        VALUES (?, ?, ?, ?)
    """, (data["case_id"], data["title"], data["total_budget"], data["total_hours"]))
    
    # 2. Iterate and insert locations and witnesses
    for city_name, loc in data["locations"].items():
        cursor.execute("""
            INSERT OR REPLACE INTO locations (case_id, city_name, country, description)
            VALUES (?, ?, ?, ?)
        """, (data["case_id"], loc["city_name"], loc["country"], loc["description"]))
        
        for witness in loc["witnesses"]:
            cursor.execute("""
                INSERT INTO clues (case_id, city_name, witness_role, personality, clue_text, fake_clue_text, bribe_cost, failed_text, is_locked)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["case_id"],
                loc["city_name"],
                witness["role"],
                witness["personality"],
                witness["clue_text"],
                witness["fake_clue_text"],
                witness["bribe_cost"],
                witness["failed_text"],
                1 if witness["is_locked"] else 0  # SQLite uses 1/0 for Booleans
            ))
            
    conn.commit()
    conn.close()
    print(f"Successfully imported Lacy La Case: {data['title']}!")

if __name__ == "__main__":
    import_case_data()