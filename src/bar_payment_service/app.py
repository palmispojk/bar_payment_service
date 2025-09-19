from flask import Flask
import os, sqlite3
from db_handling import db_init, db_config
from .routes import index_bp, confirm_order_bp


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
app.register_blueprint(index_bp)
app.register_blueprint(confirm_order_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)