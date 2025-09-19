// ============================
// Cart Utility Functions
// ============================

/**
 * Break quantities into specials + leftovers
 * @param {string} drinkName
 * @param {number} qty
 * @param {Array} drinks - list of all drinks with {name, price}
 * @param {Object} specialsData - specials map { drinkName: [{quantity, price}, ...] }
 * @returns {Array} rows with {label, displayQty, drinkQty, price}
 */

export function breakdownWithSpecials(drinkName, qty, drinks, specialsData) {
    const drinkData = drinks.find(d => d.name === drinkName);
    if (!drinkData) return [];

    const basePrice = drinkData.price;
    const specials = specialsData[drinkName] || [];

    let rows = [];
    let remaining = qty;

    specials.sort((a, b) => b.quantity - a.quantity);

    for (const deal of specials) {
        const count = Math.floor(remaining / deal.quantity);
        if (count > 0) {
            remaining -= count * deal.quantity;
            rows.push({
                label: `${deal.quantity} ${drinkName} (special)`,
                displayQty: count,
                drinkQty: count * deal.quantity,
                price: count * deal.price
            });
        }
    }

    if (remaining > 0) {
        rows.push({
            label: drinkName,
            displayQty: remaining,
            drinkQty: remaining,
            price: remaining * basePrice
        });
    }

    return rows;
}

/**
 * Compute total price and total quantity for a cart
 */
export function computeTotals(cart, drinks, specialsData) {
    let totalPrice = 0;
    let totalQty = 0;

    Object.entries(cart).forEach(([name, qty]) => {
        const rows = breakdownWithSpecials(name, qty, drinks, specialsData);
        rows.forEach(r => {
            totalPrice += r.price;
            totalQty += r.drinkQty;
        });
    });

    return { totalPrice, totalQty };
}
