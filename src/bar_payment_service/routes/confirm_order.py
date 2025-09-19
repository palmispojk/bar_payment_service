from flask import Blueprint, render_template, request, session, redirect, url_for
import json
from env import DB_FILE_PATH
from db_handling.db_utils import get_specials_and_drinks
from db_handling.db_orders import create_order

confirm_order_bp = Blueprint("confirm_order", __name__)


@confirm_order_bp.route("/confirm-order", methods=["GET"], strict_slashes=False)
def confirm_order():
    
    drinks, specials = get_specials_and_drinks(DB_FILE_PATH)
    return render_template(
        "confirm_order.html",
        drinks=drinks,
        specials=json.dumps(specials)
    )



@confirm_order_bp.route("/finalize-order", methods=["POST"], strict_slashes=False)
def finalize_order():
    data = request.get_json()
    cart_items = data["cart"]
    create_order(DB_FILE_PATH, cart_items)
    return "Order added to database", 200