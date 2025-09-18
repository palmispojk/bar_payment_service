from flask import Flask
import os
from . import db


app = Flask(__name__)

# --------------------------
# Initialize database
# --------------------------
DB_FOLDER = "database"
DB_FILE_PATH = os.path.join(DB_FOLDER, "bar.db")
DB_PRICES_PATH = os.path.join(DB_FOLDER, "prices.json")

db.init_drinks(DB_FILE_PATH)
db.update_prices_from_json(DB_FILE_PATH, DB_PRICES_PATH)

@app.route("/")
def index():
    con = db.sqlite3.connect(DB_FILE_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, name, price FROM drinks")
    drinks = cur.fetchall()
    con.close()

    html = "<h1>Dorm Bar Menu</h1><ul>"
    for d in drinks:
        html += f"<li>{d[1]} - {d[2]} DKK</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(debug=True)