// ============================
// Dorm Bar Front-End Cart
// ============================

// Cart stored entirely in front-end
let cart = {};
let totalPrice = 0;
let totalQty = 0;

// ----------------------------
// Create buttons for all drinks
// ----------------------------
const buttonsDiv = document.getElementById('buttons');

drinks.forEach(d => {
    const btn = document.createElement('button');
    btn.textContent = `${d.name} - ${d.price} DKK`;
    btn.onclick = () => {
        cart[d.name] = (cart[d.name] || 0) + 1;
        updateCart();
    };
    buttonsDiv.appendChild(btn);
});

// ============================
// Utility: Calculate price with specials
// ============================
function calculatePriceWithSpecials(drinkName, qty) {
    const drinkData = drinks.find(d => d.name === drinkName);
    const basePrice = drinkData.price;

    // Specials list for this drink
    const specials = specialsData[drinkName] || [];  
    // Example: specialsData = { "Shot": [{quantity: 10, price: 85}], "Beer": [...] }

    let remaining = qty;
    let total = 0;

    // Sort specials by largest quantity first (greedy approach)
    specials.sort((a, b) => b.quantity - a.quantity);

    for (const deal of specials) {
        while (remaining >= deal.quantity) {
            remaining -= deal.quantity;
            total += deal.price;
        }
    }

    // Add leftovers at normal price
    total += remaining * basePrice;

    return total;
}


// ----------------------------
// Update cart table
// ----------------------------
function updateCart() {
    const table = document.getElementById('cart-table');
    table.innerHTML = `<tr><th>Drink</th><th>Quantity</th><th>Price</th></tr>`;

    totalPrice = 0;
    totalQty = 0;

    for (let [name, qty] of Object.entries(cart)) {
        const drinkTotal = calculatePriceWithSpecials(name, qty);

        totalPrice += drinkTotal;
        totalQty += qty;

        const row = table.insertRow();
        row.insertCell(0).textContent = name;

        // Quantity cell
        const qtyCell = row.insertCell(1);
        qtyCell.className = "quantity-cell";

        const wrapper = document.createElement("div");
        wrapper.className = "qty-wrapper";

        const qtySpan = document.createElement("span");
        qtySpan.textContent = qty;
        qtySpan.className = "qty-number";
        wrapper.appendChild(qtySpan);

        const decBtn = document.createElement('button');
        decBtn.textContent = "−";
        decBtn.className = "small-btn";
        decBtn.onclick = () => {
            cart[name] -= 1;
            if (cart[name] <= 0) delete cart[name];
            updateCart();
        };
        wrapper.appendChild(decBtn);

        qtyCell.appendChild(wrapper);

        // Price cell (with specials applied)
        const priceCell = row.insertCell(2);
        priceCell.textContent = drinkTotal + " DKK";
        priceCell.className = "price-cell";
    }

    // Total row
    const totalRow = table.insertRow();
    totalRow.insertCell(0).textContent = "Total";
    totalRow.insertCell(1).textContent = totalQty;
    totalRow.insertCell(2).textContent = totalPrice + " DKK";
}


// Initialize table at page load
updateCart();

// ----------------------------
// Place Order Button Handler
// ----------------------------
document.getElementById('place-order').onclick = () => {
    if (totalQty === 0) {
        alert("Your cart is empty!");
        return;
    }

    let summary = "Order submitted!\n\n";
    for (let [name, qty] of Object.entries(cart)) {
        const pricePerItem = drinks.find(d => d.name === name).price;
        summary += `${name}: ${qty} × ${pricePerItem} DKK = ${qty * pricePerItem} DKK\n`;
    }
    summary += `\nTotal items: ${totalQty}\nTotal price: ${totalPrice} DKK`;

    alert(summary);

    // Clear cart after placing order
    cart = {};
    updateCart();
};

// ----------------------------
// Clear Table Button Handler
// ----------------------------
document.getElementById('clear-table').onclick = () => {
    cart = {};
    updateCart();
};
