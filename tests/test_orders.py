import sqlite3
from db_handling import db_orders
from .helpers import add_special, get_drink_id, place_order, expected_rows_orders, calculate_expected_total


def test_create_one_order_inserts_order_row(setup_and_teardown):
    """Test that creating an order inserts one row in orders table."""
    db_path = setup_and_teardown
    items = {"Beer": 3, "Shot": 2}

    _, _ = db_orders.create_order(db_path, items)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM orders")
    count = cur.fetchone()[0]
    con.close()

    assert count == 1, "One order row should be created"


def test_create_one_order_inserts_correct_order_items(setup_and_teardown):
    """Test that creating an order inserts correct number of rows in order_items table."""
    db_path = setup_and_teardown
    items = {"Beer": 3, "Shot": 2}

    order_id, _ = db_orders.create_order(db_path, items)

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (order_id,))
    count = cur.fetchone()[0]
    con.close()

    assert count == len(items), "Order items rows should match number of different drinks"


def test_create_one_order_calculates_total_correctly(setup_and_teardown):
    """Test that total_price of the order matches sum of item prices."""
    db_path = setup_and_teardown
    items = {"Beer": 3, "Shot": 2}

    order_id, total_price = db_orders.create_order(db_path, items)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("SELECT name, price FROM drinks")
    drink_prices = dict(cur.fetchall())  # {name: price}

    expected_total = sum(drink_prices[name] * quantity for name, quantity in items.items())

    assert total_price == expected_total, "Returned total_price should match calculated total"

    cur.execute("SELECT total_price FROM orders WHERE id = ?", (order_id,))
    db_total = cur.fetchone()[0]
    con.close()

    assert db_total == expected_total, "Database total_price should match expected total"



def test_single_special(reset_db):
    """Test a single special, shot is in deal and beer is normal, see if num rows is correct and total price"""
    db_path = reset_db

    shot_id = get_drink_id(db_path, "Shot")
    special_shot_price = 85
    special_shot_quantity = 10
    add_special(db_path, shot_id, quantity=special_shot_quantity, price=special_shot_price)
    
    beer_id = get_drink_id(db_path, "Beer")

    num_shots = 12
    num_beers = 3
    items = {"Shot": num_shots, "Beer": num_beers}
    _, total_price, rows = place_order(db_path, items)

    shot_rows = [r for r in rows if r[0] == shot_id]
    beer_rows = [r for r in rows if r[0] == beer_id]
    
    expected_rows_shots = expected_rows_orders(num_shots, [special_shot_quantity])
    assert len(shot_rows) == expected_rows_shots, "Should return the correct amount of rows in ordered items for the amount of shots."
    
    expected_rows_beers = expected_rows_orders(num_beers, [])
    assert len(beer_rows) == expected_rows_beers, "Should return the correct amount of rows in ordered items for the amount of beers."
    

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT price FROM drinks WHERE id = ?", (shot_id,))
    regular_shot_price = cur.fetchone()[0]
    cur.execute("SELECT price FROM drinks WHERE id = ?", (beer_id,))
    beer_price = cur.fetchone()[0]
    con.close()

    expected_total_cost_shots = calculate_expected_total(num_shots, regular_shot_price, {special_shot_quantity: special_shot_price})
    expected_total_cost_beers = calculate_expected_total(num_beers, beer_price, {})
    assert total_price == expected_total_cost_shots + expected_total_cost_beers, "The total cost inside the system should be equal to the cost inside the database."


def test_multiple_specials(reset_db):
    """Test a single special, shot  and beer is deal, see if num rows is correct and total price"""
    db_path = reset_db

    # Prepare specials
    shot_id = get_drink_id(db_path, "Shot")
    special_shot_price = 85
    special_shot_quantity = 10
    beer_id = get_drink_id(db_path, "Beer")
    special_beer_price = 100
    special_beer_quantity = 7
    add_special(db_path, shot_id, quantity=special_shot_quantity, price=special_shot_price)
    add_special(db_path, beer_id, quantity=special_beer_quantity, price=special_beer_price)

    num_beers = 12
    num_shots = 12
    items = {"Shot": num_shots, "Beer": num_beers}
    _, total_price, rows = place_order(db_path, items)

    shot_rows = [r for r in rows if r[0] == shot_id]
    beer_rows = [r for r in rows if r[0] == beer_id]
    
    expected_rows_shots = expected_rows_orders(num_shots, [special_shot_quantity])
    assert len(shot_rows) == expected_rows_shots, "Should return the correct amount of rows in ordered items for the amount of shots."
    
    expected_rows_beers = expected_rows_orders(num_beers, [special_beer_quantity])
    assert len(beer_rows) == expected_rows_beers, "Should return the correct amount of rows in ordered items for the amount of beers."

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT price FROM drinks WHERE id = ?", (shot_id,))
    regular_shot_price = cur.fetchone()[0]
    cur.execute("SELECT price FROM drinks WHERE id = ?", (beer_id,))
    beer_price = cur.fetchone()[0]
    con.close()

    expected_total_cost_shots = calculate_expected_total(num_shots, regular_shot_price, {special_shot_quantity: special_shot_price})
    expected_total_cost_beers = calculate_expected_total(num_beers, beer_price, {special_beer_quantity: special_beer_price})
    assert total_price == expected_total_cost_shots + expected_total_cost_beers, "The total cost inside the system should be equal to the cost inside the database."