import sqlite3
import os, json

def init_drinks(db_path: str):
    """Create the drinks table if it does not exist."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS drinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    """)
    con.commit()
    con.close()
    

def update_prices_from_json(db_path: str, json_file: str):
    """Update the drinks table to match JSON prices."""
    if not os.path.exists(json_file):
        print(f"{json_file} not found, skipping price update.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        prices = json.load(f)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for name, price in prices.items():
        # Insert new drinks or update price if drink exists
        cur.execute("""
            INSERT INTO drinks (name, price)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET price=excluded.price
        """, (name, price))
    con.commit()
    con.close()