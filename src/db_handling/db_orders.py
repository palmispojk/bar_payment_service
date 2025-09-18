import sqlite3

def create_order(db_path: str, items: dict) -> tuple[int, float]:
    """
    Create an order considering special prices.

    items = {
        "Beer": 3,
        "Shot": 12  # if special: 10 for 85
    }

    Returns: (order_id, total_price)
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    total_price = 0.0
    order_rows = []

    for drink_name, quantity in items.items():
        # Get active drink info
        cur.execute(
            "SELECT id, price FROM drinks WHERE name = ? AND active = 1",
            (drink_name,)
        )
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Active drink with name '{drink_name}' does not exist")
        drink_id, normal_price = row

        # Check for active specials, ordered by quantity descending
        cur.execute(
            "SELECT id, quantity, price FROM specials WHERE drink_id = ? AND active = 1 ORDER BY quantity DESC",
            (drink_id,)
        )
        specials = cur.fetchall()  # list of (special_id, special_qty, special_price)

        remaining_qty = quantity

        # Apply specials greedily
        for special_id, special_qty, special_price in specials:
            num_specials = remaining_qty // special_qty
            if num_specials > 0:
                order_rows.append((drink_id, num_specials * special_qty, special_price, special_id))
                total_price += num_specials * special_price
                remaining_qty -= num_specials * special_qty

        # Remaining items at normal price
        if remaining_qty > 0:
            order_rows.append((drink_id, remaining_qty, normal_price, None))
            total_price += remaining_qty * normal_price

    # Insert order
    cur.execute("INSERT INTO orders (total_price) VALUES (?)", (total_price,))
    order_id = cur.lastrowid

    # Insert order items
    for drink_id, quantity, price, special_id in order_rows:
        cur.execute(
            """
            INSERT INTO order_items (order_id, drink_id, quantity, price, special_price_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (order_id, drink_id, quantity, price, special_id)
        )

    con.commit()
    con.close()
    return order_id, total_price
