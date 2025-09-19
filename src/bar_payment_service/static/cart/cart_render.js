import { breakdownWithSpecials, computeTotals } from './cart_utils.js';

/**
 * Render the cart table
 */
function renderCartRows(cart, drinks, specialsData, table) {
    table.innerHTML = `<tr><th>Drink</th><th>Quantity</th><th>Price</th></tr>`;

    Object.entries(cart).forEach(([name, qty]) => {
        const rows = breakdownWithSpecials(name, qty, drinks, specialsData);

        rows.forEach(r => {
            const row = table.insertRow();
            row.insertCell(0).textContent = r.label;

            const qtyCell = row.insertCell(1);
            const wrapper = document.createElement("div");
            wrapper.className = "qty-wrapper";

            const qtySpan = document.createElement("span");
            qtySpan.textContent = r.displayQty;
            qtySpan.className = "qty-number";
            wrapper.appendChild(qtySpan);

            qtyCell.appendChild(wrapper);

            const priceCell = row.insertCell(2);
            priceCell.textContent = r.price + " DKK";
            priceCell.className = "price-cell";
        });
    });

    const totals = computeTotals(cart, drinks, specialsData);
    const totalRow = table.insertRow();
    totalRow.insertCell(0).textContent = "Total";
    totalRow.insertCell(1).textContent = totals.totalQty;
    totalRow.insertCell(2).textContent = totals.totalPrice + " DKK";
}


export function renderEditableCartTable(cart, drinks, specialsData, tableId='cart-table') {
    const table = document.getElementById(tableId);
    if (!table) return;

    renderCartRows(cart, drinks, specialsData, table);

    // Attach decrement buttons
    table.querySelectorAll('.qty-wrapper').forEach((wrapper, index) => {
        const name = Object.keys(cart)[Math.floor(index / 1)]; // depends on rows per item
        const decBtn = document.createElement('button');
        decBtn.textContent = '−';
        decBtn.className = 'small-btn';
        decBtn.onclick = () => {
            cart[name] -= 1;
            if (cart[name] <= 0) delete cart[name];
            localStorage.setItem('cart', JSON.stringify(cart));
            renderEditableCartTable(cart, drinks, specialsData, tableId);
        };
        wrapper.appendChild(decBtn);
    });
}


export function renderStaticCartTable(cart, drinks, specialsData, tableId='cart-table') {
    const table = document.getElementById(tableId);
    if (!table) return;

    renderCartRows(cart, drinks, specialsData, table);
}

