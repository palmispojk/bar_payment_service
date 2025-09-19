import os

# PROJECT_ROOT is the folder where this file lives
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Database folder and files
DB_FOLDER = os.path.join(PROJECT_ROOT, "database")
DB_FILE_PATH = os.path.join(DB_FOLDER, "bar.db")
PRICES_FILE_PATH = os.path.join(DB_FOLDER, "prices.json")
