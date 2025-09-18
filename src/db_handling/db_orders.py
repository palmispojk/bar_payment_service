
import sqlite3

def create_order(db_path: str, items: dict) -> tuple[int, float]:
    """
    Create an order with multiple drink items.

    items = [
        {"Beer": 3},
        {"Shot": 2}
    ]

    Returns: (order_id, total_price)
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    total_price = 0.0

    # Calculate total and record items
    for drink_name, quantity in items.items():
        cur.execute("SELECT price FROM drinks WHERE name = ?", (drink_name,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Drink with name {drink_name} does not exist")

        price = row[0]
        line_total = price * quantity
        total_price += line_total


    # Insert order row
    cur.execute(
    "INSERT INTO orders (total_price) VALUES (?)",
    (total_price,),
    )
    
    order_id = cur.lastrowid

    # Insert each item row
    for drink_name, quantity in items.items():
        cur.execute("SELECT price FROM drinks WHERE name = ?", (drink_name,))
        price = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO order_items (order_id, drink_name, quantity, price)
            VALUES (?, ?, ?, ?)
            """,
            (order_id, drink_name, quantity, price),
        )

    con.commit()
    con.close()

    return order_id, total_price