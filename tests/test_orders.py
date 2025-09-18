# tests/test_orders.py

import sqlite3
from db_handling import db_orders

def test_create_order_with_multiple_items(setup_and_teardown):
    db_path = setup_and_teardown

    items = {
        "Beer": 3,
        "Shot": 2
    }

    order_id, total_price = db_orders.create_order(db_path, items)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM orders")
    assert cur.fetchone()[0] == 1

    cur.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (order_id,))
    assert cur.fetchone()[0] == len(items)

    cur.execute("SELECT name, price FROM drinks")
    drink_prices = dict(cur.fetchall())  # {name: price}

    expected_total = sum(drink_prices[name] * quantity for name, quantity in items.items())

    assert total_price == expected_total

    cur.execute("SELECT total_price FROM orders WHERE id = ?", (order_id,))
    db_total = cur.fetchone()[0]
    assert db_total == expected_total

    con.close()
