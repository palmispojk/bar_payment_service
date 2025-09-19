from flask import Blueprint, render_template, request, jsonify
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
    """Finalize an order and save it to the database."""
    data = request.get_json(silent=True)

    if not data or "cart" not in data:
        return jsonify({"error": "Missing cart data"}), 400

    cart_items = data["cart"]

    try:
        create_order(DB_FILE_PATH, cart_items)
        return jsonify({"message": "Order successfully added to database"}), 201
    except Exception as e:
        # Log error internally if needed
        print(f"Error finalizing order: {e}")
        return jsonify({"error": "Failed to finalize order"}), 500


@confirm_order_bp.route("/confirmed", methods=["GET"], strict_slashes=False)
def confirmed():
    """Show a simple confirmation page after successful order."""
    return render_template("confirmed.html")
