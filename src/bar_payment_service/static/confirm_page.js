import { breakdownWithSpecials } from './cart/cart_utils.js';
import { renderStaticCartTable } from './cart/cart_render.js';

// Load cart from localStorage
let cart = JSON.parse(localStorage.getItem("cart") || "{}");

// Render table using shared module
renderStaticCartTable(cart, drinks, specialsData, "cart-table");

// Calculate totals
let totalPrice = Object.entries(cart).reduce((sum, [name, qty]) => {
    const rows = breakdownWithSpecials(name, qty, drinks, specialsData);
    return sum + rows.reduce((rSum, r) => rSum + r.price, 0);
}, 0);

let totalQty = Object.entries(cart).reduce((sum, [name, qty]) => {
    const rows = breakdownWithSpecials(name, qty, drinks, specialsData);
    return sum + rows.reduce((rSum, r) => rSum + r.drinkQty, 0);
}, 0);

// Confirm order button
document.getElementById("confirm-order").onclick = async (e) => {
    if (totalQty === 0) {
        alert("Cart is empty!");
        return;
    }

    const finalizeUrl = e.target.dataset.finalizeUrl;

    const response = await fetch(finalizeUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cart })
    });

    if (response.ok) {
        localStorage.removeItem("cart"); // clear cart after order
        window.location.href = "/thankyou";
    } else {
        alert("Error finalizing order. Try again.");
    }
};

// Back to menu button
document.getElementById("back-to-menu").onclick = (e) => {
    window.location.href = e.target.dataset.indexUrl;
};
