import sqlite3
from typing import Tuple, Any

def get_specials_and_drinks(db_file_path: str) -> Tuple[list[dict], dict]:
    
    
    con = sqlite3.connect(db_file_path)
    cur = con.cursor()

    # --- Fetch active drinks ---
    cur.execute("SELECT id, name, price FROM drinks WHERE active = 1")
    drinks = [{"id": row[0], "name": row[1], "price": row[2]} for row in cur.fetchall()]

    # --- Fetch active specials ---
    cur.execute("""
        SELECT s.drink_id, d.name, s.quantity, s.price
        FROM specials s
        JOIN drinks d ON s.drink_id = d.id
        WHERE s.active = 1
    """)
    
    specials = {}
    for drink_id, name, quantity, price in cur.fetchall():
        if name not in specials:
            specials[name] = []
        specials[name].append({"drink_id": drink_id, "quantity": quantity, "price": price})

    con.close()
    return drinks, specials