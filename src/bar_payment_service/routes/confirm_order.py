from flask import Blueprint, render_template, request, session, redirect, url_for
import json
from db_handling.db_config import DB_FILE_PATH
from db_handling.db_utils import get_specials_and_drinks

confirm_order_bp = Blueprint("confirm_order", __name__)


@confirm_order_bp.route("/confirm-order", methods=["GET"], strict_slashes=False)
def confirm_order():
    
    drinks, specials = get_specials_and_drinks(DB_FILE_PATH)
    return render_template(
        "confirm_order.html",
        drinks=drinks,
        specials=json.dumps(specials)
    )



@confirm_order_bp.route("/finalize-order", methods=["GET"], strict_slashes=False)
def finalize_order():
    data = request.get_json()
    return 200