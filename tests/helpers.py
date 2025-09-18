import sqlite3
from db_handling import db_orders

def clear_table(db_path: str, table: str):
    """Delete all rows from a table."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table}")
    con.commit()
    con.close()

def add_special(db_path: str, drink_id: int, quantity: int, price: float, active: bool = True):
    """Insert a special offer for a drink. Deactivate any existing specials for this drink."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Deactivate existing specials for this drink
    cur.execute("UPDATE specials SET active = 0 WHERE drink_id = ?", (drink_id,))

    # Insert new special
    cur.execute("""
        INSERT INTO specials (drink_id, quantity, price, active)
        VALUES (?, ?, ?, ?)
    """, (drink_id, quantity, price, int(active)))

    con.commit()
    con.close()

def get_drink_id(db_path: str, name: str) -> int:
    """Return the ID of an active drink by name."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT id FROM drinks WHERE name = ? AND active = 1", (name,))
    row = cur.fetchone()
    con.close()
    if not row:
        raise ValueError(f"Active drink '{name}' not found")
    return row[0]


def clear_all(db_path: str):
    """Clear orders, order_items, and specials."""
    for table in ["orders", "order_items", "specials"]:
        clear_table(db_path, table)


def place_order(db_path, items):
    """Helper to place an order and return rows for easier assertions."""
    order_id, total_price = db_orders.create_order(db_path, items)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT drink_id, quantity, price FROM order_items WHERE order_id = ?", (order_id,))
    rows = cur.fetchall()
    con.close()
    return order_id, total_price, rows

def expected_rows_orders(quantity: int, deal_quantities: list[int]) -> int:
    """The expected amount of rows for ordered items

    Args:
        quantity (int): The amount of one type being purchased.
        deal_quantity (list[int]): A list of the deals that are possible for one type.

    Returns:
        int: The total amount of rows being entered in to the database.
    """
    num_rows_expected = 0
    deal_quantities = sorted(deal_quantities, reverse=True)

    remaining = quantity
    for deal in deal_quantities:
        if remaining >= deal:
            # Count a single row for all specials that fit this deal
            num_specials = remaining // deal
            if num_specials > 0:
                num_rows_expected += 1  # combined into a single row
                remaining -= num_specials * deal

    # Any leftover quantity counts as one normal row
    if remaining > 0:
        num_rows_expected += 1

    return num_rows_expected


def calculate_expected_total(quantity: int, normal_price: float, specials: dict[int, float]) -> float:
    """
    Calculate the expected total price given quantity, normal price, and specials.

    Args:
        quantity (int): Total number of drinks being purchased.
        normal_price (float): Regular price of one unit.
        specials (dict[int, float]): Mapping of special quantity -> special price. E.g., {10: 85}

    Returns:
        float: The expected total price.
    """
    total = 0
    remaining = quantity

    # Apply specials in descending order of quantity
    for deal_qty in sorted(specials.keys(), reverse=True):
        deal_price = specials[deal_qty]
        num_deals = remaining // deal_qty
        if num_deals > 0:
            total += num_deals * deal_price
            remaining -= num_deals * deal_qty

    # Add remaining at normal price
    total += remaining * normal_price
    return total
