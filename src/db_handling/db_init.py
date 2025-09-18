import sqlite3
import os, json


def init_drinks(db_path: str):
    """Create the drinks table and specials table if they do not exist."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Regular drinks table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS drinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    # Special prices table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS specials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drink_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(drink_id) REFERENCES drinks(id)
        )
        """
    )

    con.commit()
    con.close()


def update_prices_from_json(db_path: str, json_file: str):
    """Update drinks so JSON drinks are active.
    If a price changes for the same name, old row becomes inactive and a new row is inserted.
    """
    if not os.path.exists(json_file):
        print(f"{json_file} not found, skipping price update.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    regular_prices = data.get("regular", {})
    special_prices = data.get("special", {})

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Processing Regular drinks
    cur.execute("UPDATE drinks SET active = 0")
    
    for name, price in regular_prices.items():
        cur.execute(
            "SELECT id FROM drinks WHERE name = ? AND price = ?",
            (name, price),
        )
        row = cur.fetchone()

        if row:
            # Already exists with same price → keep it active
            cur.execute("UPDATE drinks SET active = 1 WHERE id = ?", (row[0],))
        else:
            # Insert new version, mark active
            cur.execute(
                "INSERT INTO drinks (name, price, active) VALUES (?, ?, 1)",
                (name, price),
            )
    
    cur.execute("UPDATE specials SET active = 0")
    
    for drink_name, info in special_prices.items():
        quantity = info["quantity"]
        price = info["price"]
        
        cur.execute("SELECT id FROM drinks WHERE name = ? AND active = 1", (drink_name,))
        
        row = cur.fetchone()
        if not row:
            print(f"Warning: special for {drink_name} ignored (no active drink)")
            continue
        
        drink_id = row[0]
        active = 1
        cur.execute(
            "INSERT INTO specials (drink_id, quantity, price, active) VALUES (?, ?, ?, ?)",
            (drink_id, quantity, price, active),
        )

    con.commit()
    con.close()


def init_orders(db_path: str):
    """Create tables for orders and order items, supporting special prices."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Orders table (one row per order)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_price REAL NOT NULL
        )
    """)

    # Order items table (multiple rows per order)
    # special_price_id is NULL if no special was applied
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            drink_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            special_price_id INTEGER DEFAULT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(drink_id) REFERENCES drinks(id),
            FOREIGN KEY(special_price_id) REFERENCES specials(id)
        )
    """)

    con.commit()
    con.close()
