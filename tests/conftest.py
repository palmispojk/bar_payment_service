# tests/conftest.py
import os
import sqlite3
import pytest
from db_handling import db_init

TEST_DB = "test_bar.db"

@pytest.fixture
def setup_and_teardown():
    # Remove old DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db_init.init_drinks(TEST_DB)
    db_init.init_orders(TEST_DB)

    con = sqlite3.connect(TEST_DB)
    cur = con.cursor()
    cur.execute("INSERT INTO drinks (name, price) VALUES (?, ?)", ("Beer", 20))
    cur.execute("INSERT INTO drinks (name, price) VALUES (?, ?)", ("Shot", 15))
    con.commit()
    con.close()

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
