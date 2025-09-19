from flask import Blueprint, render_template, session
import json
from env import DB_FILE_PATH
from db_handling.db_utils import get_specials_and_drinks

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET"])
def index():
    drinks, specials = get_specials_and_drinks(DB_FILE_PATH)
    
    return render_template(
        "index.html",
        drinks=drinks,
        specials=json.dumps(specials)
    )
