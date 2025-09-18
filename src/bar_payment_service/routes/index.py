from flask import Blueprint, render_template
import sqlite3
from db_handling.db_config import DB_FILE_PATH

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    # Fetch drinks from database
    con = sqlite3.connect(DB_FILE_PATH)
    cur = con.cursor()
    cur.execute("SELECT name, price FROM drinks")
    rows = cur.fetchall()
    con.close()

    drinks = [{"name": row[0], "price": row[1]} for row in rows]

    return render_template("index.html", drinks=drinks)
