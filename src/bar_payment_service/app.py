from flask import Flask
import os, sqlite3
from db_handling import db_init
from .routes import index_bp, confirm_order_bp
import env


app = Flask(__name__)

# --------------------------
# Initialize database
# --------------------------

db_init.init_drinks(env.DB_FILE_PATH)
db_init.update_prices_from_json(env.DB_FILE_PATH, env.PRICES_FILE_PATH)
db_init.init_orders(env.DB_FILE_PATH)

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