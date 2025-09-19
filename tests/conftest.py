# tests/conftest.py
import os
import sqlite3
import pytest
from db_handling import db_init
from .helpers import clear_all

TEST_DB = "test_bar.db"

ITEMS_PRICES = {
    "Beer": 20.0,
    "Shot": 15.0
}

@pytest.fixture
def setup_and_teardown():
    # Remove old DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db_init.init_drinks(TEST_DB)
    db_init.init_orders(TEST_DB)

    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("INSERT INTO drinks (name, price) VALUES (?, ?)", ("Beer", ITEMS_PRICES["Beer"]))
    cur.execute("INSERT INTO drinks (name, price) VALUES (?, ?)", ("Shot", ITEMS_PRICES["Shot"]))
    con.commit()
    con.close()

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def reset_db(setup_and_teardown):
    """Reset DB before each test."""
    db_path = setup_and_teardown
    clear_all(db_path)
    return db_path
