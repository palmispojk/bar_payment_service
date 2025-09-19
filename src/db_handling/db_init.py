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

def update_regular_drinks(cur, regular_prices: dict):
    """Update regular drinks in DB based on JSON."""
    cur.execute("UPDATE drinks SET active = 0")
    for name, price in regular_prices.items():
        # Look for any existing row with the same name and price
        cur.execute("SELECT id FROM drinks WHERE name = ? AND price = ?", (name, price))
        row = cur.fetchone()

        if row:
            # Same price exists → activate
            cur.execute("UPDATE drinks SET active = 1 WHERE id = ?", (row[0],))
        else:
            # Price changed or new → insert new active row
            cur.execute("INSERT INTO drinks (name, price, active) VALUES (?, ?, 1)", (name, price))


def update_specials(cur, special_prices: dict):
    """
    Update specials in DB based on JSON.
    Each special is for a single drink.
    """

    # Deactivate all existing specials first
    cur.execute("UPDATE specials SET active = 0")

    for drink_name, info in special_prices.items():
        quantity = info["quantity"]
        price = info["price"]

        # Get the active drink
        cur.execute("SELECT id FROM drinks WHERE name = ? AND active = 1", (drink_name,))
        row = cur.fetchone()
        if not row:
            print(f"Warning: special for '{drink_name}' ignored (no active drink)")
            continue

        drink_id = row[0]

        # Check if the same special already exists
        cur.execute(
            "SELECT id FROM specials WHERE drink_id = ? AND quantity = ? AND price = ?",
            (drink_id, quantity, price)
        )
        special_row = cur.fetchone()

        if special_row:
            # Activate existing special
            cur.execute("UPDATE specials SET active = 1 WHERE id = ?", (special_row[0],))
        else:
            # Insert new special
            cur.execute(
                "INSERT INTO specials (drink_id, quantity, price, active) VALUES (?, ?, ?, 1)",
                (drink_id, quantity, price)
            )

def update_prices_from_json(db_path: str, json_file: str):
    """Update drinks and specials from a JSON file."""
    if not os.path.exists(json_file):
        print(f"{json_file} not found, skipping price update.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    regular_prices = data.get("regular", {})
    special_prices = data.get("special", {})

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Update drinks and specials
    update_regular_drinks(cur, regular_prices)
    update_specials(cur, special_prices)

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
