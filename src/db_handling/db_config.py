import os

# Project root = parent of src/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Database folder at same level as src
DB_FOLDER = os.path.join(PROJECT_ROOT, "database")
DB_FILE_PATH = os.path.join(DB_FOLDER, "bar.db")
PRICES_FILE_PATH = os.path.join(DB_FOLDER, "prices.json")
