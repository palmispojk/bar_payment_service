import sqlite3
import json
import os
from db_handling import update_prices_from_json
from .conftest import ITEMS_PRICES


def test_update_prices_from_json_activates_existing(reset_db):
    db_path = reset_db
    test_json_path = "./tests/test.json"

    # JSON input with same prices → should just activate existing rows
    data = {
        "regular": {
            "Beer": 10.0,
            "Shot": 12.0
        }
    }
    with open(test_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # First, deactivate everything to simulate old data
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE drinks SET active = 0")
    con.commit()
    con.close()

    # Run function
    update_prices_from_json(db_path, test_json_path)

    # Check that existing rows were activated
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name, price, active FROM drinks WHERE active = 1 ORDER BY name")
    rows = cur.fetchall()
    con.close()

    expected = [("Beer", data["regular"]["Beer"], 1), ("Shot", data["regular"]["Shot"], 1)]
    assert rows == expected


def test_update_prices_from_json_inserts_new_on_price_change(reset_db):
    db_path = reset_db
    test_json_path = "./tests/test.json"
    # JSON input changes Coke price → new row should be inserted
    data = {
        "regular": {
            "Beer": 10,
            "Shot": 12
        }
    }
    with open(test_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # Run function
    update_prices_from_json(db_path, test_json_path)

    # Fetch all rows
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name, price, active FROM drinks WHERE name = ? AND active = 0", ("Beer",))
    beer_inactive = cur.fetchall()
    cur.execute("SELECT name, price, active FROM drinks WHERE name = ? AND active = 1", ("Beer",))
    beer_active = cur.fetchall()
    con.close()

    # There should be two rows for Beer: old inactive, new active
    assert len(beer_inactive) == 1
    # Old price inactive
    assert beer_inactive[0][1] == ITEMS_PRICES["Beer"] and beer_inactive[0][2] == 0
    # New price active
    assert beer_active[0][1] == data["regular"]["Beer"] and beer_active[0][2] == 1

def test_update_specials_inserts_new_on_price_change(reset_db):
    db_path = reset_db
    test_json_path = "./tests/test.json"

    # JSON input creates a special for Beer
    data = {
        "regular": {
            "Beer": 20
        },
        "special": {
            "Beer": {
                "quantity": 5,
                "price": 90  # new price
            }
        }
    }
    
    with open(test_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # Run function
    update_prices_from_json(db_path, test_json_path)

    # Fetch all specials for Beer
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "SELECT s.quantity, s.price, s.active "
        "FROM specials s "
        "JOIN drinks d ON s.drink_id = d.id "
        "WHERE d.name = ?",
        ("Beer",)
    )
    beer_specials = cur.fetchall()
    con.close()

    # There should be one active special
    assert len(beer_specials) == 1
    assert beer_specials[0][0] == data["special"]["Beer"]["quantity"]
    assert beer_specials[0][1] == data["special"]["Beer"]["price"]
    assert beer_specials[0][2] == 1  # active
