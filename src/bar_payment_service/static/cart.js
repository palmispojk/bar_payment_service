// Cart stored entirely in front-end
let cart = {};

// Create buttons for all drinks
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

// Update cart table
function updateCart() {
    const table = document.getElementById('cart-table');
    table.innerHTML = `<tr><th>Drink</th><th>Quantity</th><th>Price</th></tr>`;

    let totalPrice = 0;
    let totalQty = 0;

    for (let [name, qty] of Object.entries(cart)) {
        const price = drinks.find(d => d.name === name).price * qty;
        totalPrice += price;
        totalQty += qty;

        const row = table.insertRow();
        row.insertCell(0).textContent = name;

        const qtyCell = row.insertCell(1);
        qtyCell.className = "quantity-cell";

        // Wrapper div for number + button
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

        // Price cell
        const priceCell = row.insertCell(2);
        priceCell.textContent = price + " DKK";
        priceCell.className = "price-cell";
    }

    // Add total row
    const totalRow = table.insertRow();
    totalRow.insertCell(0).textContent = "Total";
    totalRow.insertCell(1).textContent = totalQty;
    totalRow.insertCell(2).textContent = totalPrice + " DKK";
}
updateCart();

// Handle place order
document.getElementById('place-order').onclick = () => {
    alert("Order submitted!\n" + JSON.stringify(cart));
    cart = {};
    updateCart();
};
