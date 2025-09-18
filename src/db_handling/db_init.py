import sqlite3
import os, json

def init_drinks(db_path: str):
    """Create the drinks table if it does not exist."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS drinks (
            name TEXT PRIMARY KEY,
            price REAL NOT NULL
        )
        """
    )

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
        
        cur.execute("""
            INSERT INTO drinks (name, price)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET price=excluded.price
        """, (name, price))

    con.commit()
    con.close()


def init_orders(db_path: str):
    """Create tables for orders and order items."""
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            drink_name INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(drink_name) REFERENCES drinks(name)
        )
    """)
    con.commit()
    con.close()
