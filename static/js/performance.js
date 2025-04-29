document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/get-performance");
    const data = await response.json();

    const tableBody = document.querySelector("#performance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><img src="${row.logo}" alt="${row.stock_name}" style="height:32px;width:32px;border-radius:4px;"></td>
            <td>${row.stock_name}</td>
            <td>${row.stock_symbol}</td>
            <td>${row.exchange}</td>
            <td>${row.quantity}</td>
            <td>${row.purchase_price.toFixed(2)}</td>
            <td>${row.actual_price.toFixed(2)}</td>
            <td>${row.profit_loss.toFixed(2)}</td>
            <td><button class="delete-btn" data-symbol="${row.stock_symbol}">Delete</button></td>
        `;
        tableBody.appendChild(tr);
    });

    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", async (e) => {
            const stockSymbol = e.target.getAttribute("data-symbol");
            const response = await fetch("/delete-stock", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ stock_symbol: stockSymbol }),
            });
            const result = await response.json();
            alert(result.message);
            location.reload();
        });
    });
});

document.getElementById("download-pdf").addEventListener("click", () => {
    window.location.href = "/download-pdf";
});