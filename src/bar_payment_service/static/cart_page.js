import { renderEditableCartTable } from './cart/cart_render.js';

// Load cart from localStorage
let cart = JSON.parse(localStorage.getItem("cart") || "{}");

// Render buttons
const buttonsDiv = document.getElementById('buttons');
drinks.forEach(d => {
    const btn = document.createElement('button');
    btn.textContent = `${d.name} - ${d.price} DKK`;
    btn.onclick = () => {
        cart[d.name] = (cart[d.name] || 0) + 1;
        renderEditableCartTable(cart, drinks, specialsData, "cart-table");
    };
    buttonsDiv.appendChild(btn);
});

// Initialize table
renderEditableCartTable(cart, drinks, specialsData, "cart-table");

// Place order
document.getElementById("place-order").onclick = () => {
    if (Object.keys(cart).length === 0) {
        alert("Your cart is empty!");
        return;
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    window.location.href = "/confirm-order";
};

// Clear table
document.getElementById('clear-table').onclick = () => {
    cart = {};
    localStorage.removeItem('cart');
    renderEditableCartTable(cart, drinks, specialsData, "cart-table");
};
