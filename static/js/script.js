document.addEventListener("DOMContentLoaded", async () => {
    // Fetch top gainers and losers
    const response = await fetch("/get-gainers-losers");
    const data = await response.json();

    const gainersList = document.getElementById("gainers-list");
    const losersList = document.getElementById("losers-list");

    // Populate Gainers
    gainersList.innerHTML = ""; // Clear existing content
    data.gainers.forEach((stock) => {
        const card = document.createElement("div");
        card.className = "stock-card";
        card.innerHTML = `
            <img src="${stock.logo}" alt="${stock.name}">
            <h3>${stock.name}</h3>
            <p>₹${stock.price.toFixed(2)}</p>
            <p class="positive">+${stock.change.toFixed(2)} (${stock.change_percent.toFixed(2)}%)</p>
        `;
        gainersList.appendChild(card);
    });

    // Populate Losers
    losersList.innerHTML = ""; // Clear existing content
    data.losers.forEach((stock) => {
        const card = document.createElement("div");
        card.className = "stock-card";
        card.innerHTML = `
            <img src="${stock.logo}" alt="${stock.name}">
            <h3>${stock.name}</h3>
            <p>₹${stock.price.toFixed(2)}</p>
            <p class="negative">${stock.change.toFixed(2)} (${stock.change_percent.toFixed(2)}%)</p>
        `;
        losersList.appendChild(card);
    });

    // Stock form submission
    const stockForm = document.getElementById("stock-form");
    if (stockForm) {
        stockForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const stockSymbol = document.getElementById("stock_symbol").value;
            const exchange = document.getElementById("exchange").value;
            const quantity = document.getElementById("quantity").value;
            const purchasePrice = document.getElementById("purchase_price").value;

            try {
                const response = await fetch("/upload", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ stock_symbol: stockSymbol, exchange, quantity, purchase_price: purchasePrice }),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    alert("Error: " + errorText);
                    return;
                }

                const result = await response.json();
                alert(result.message);
                stockForm.reset();
            } catch (err) {
                alert("Network or server error: " + err.message);
            }
        });
    }

    // Expose deleteStock globally if needed for performance page
    window.deleteStock = function(stockSymbol) {
        fetch('/delete-stock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ stock_symbol: stockSymbol })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            // Refresh the performance table/list after deletion
            if (typeof loadPerformanceData === "function") {
                loadPerformanceData();
            }
        })
        .catch(error => {
            alert('Error deleting stock.');
        });
    };
});