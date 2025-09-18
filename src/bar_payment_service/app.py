from flask import Flask
import os, sqlite3
from db_handling import db_init, db_config
from . import routes


app = Flask(__name__)

# --------------------------
# Initialize database
# --------------------------

db_init.init_drinks(db_config.DB_FILE_PATH)
db_init.update_prices_from_json(db_config.DB_FILE_PATH, db_config.PRICES_FILE_PATH)
db_init.init_orders(db_config.DB_FILE_PATH)

# --------------------------
# Routing
# --------------------------
app.secret_key = "supersecretkey"

# --------------------------
# Routing
# --------------------------
app.register_blueprint(routes.index.main_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)