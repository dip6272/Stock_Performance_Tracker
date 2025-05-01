from flask import Flask, render_template, request, jsonify, send_file
import csv
import os
import yfinance as yf
from fpdf import FPDF
from nsetools import Nse  # Backup module for NSE
import requests
import tempfile
import pandas as pd

app = Flask(__name__)

# File to store user stock data
STOCK_FILE = "user_stocks.csv"

COMPANY_NAME_TO_SYMBOL = {
    "TCS": "TCS.NS",
    "TATA CONSULTANCY SERVICES": "TCS.NS",
    "INFY": "INFY.NS",
    "INFOSYS": "INFY.NS",
    "AXIS BANK": "AXISBANK.NS",
    "AXIS BANK LIMITED": "AXISBANK.NS",
    "JSW STEEL": "JSWSTEEL.NS",
    "JSW STEEL LIMITED": "JSWSTEEL.NS",
    # Add more mappings as needed
}

def resolve_symbol(user_input):
    key = user_input.strip().upper()
    if key in COMPANY_NAME_TO_SYMBOL:
        return COMPANY_NAME_TO_SYMBOL[key]
    for name, symbol in COMPANY_NAME_TO_SYMBOL.items():
        if key in name:
            return symbol
    return user_input.upper() + ".NS"

@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Read Excel file
    df = pd.read_excel(file)

    # Copy Closing Value to Opening Value in the result
    df['Opening Value'] = df['Closing Value']

    # Add columns for actual price and profit/loss
    actual_prices = []
    profit_losses = []

    for idx, row in df.iterrows():
        symbol = str(row['Stock Symbol'])
        quantity = float(row['Quantity'])
        opening_price = float(row['Opening Value'])  # Now use the new Opening Value

        # Get today's close price from yfinance
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            if not hist.empty:
                actual_price = hist['Close'].iloc[-1]
            else:
                actual_price = None
        except Exception:
            actual_price = None

        actual_prices.append(actual_price)
        if actual_price is not None:
            profit_losses.append((actual_price - opening_price) * quantity)
        else:
            profit_losses.append(None)

    df['Actual Price'] = actual_prices
    df['Profit/Loss'] = profit_losses

    # Save to a temporary Excel file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False)
        tmp_path = tmp.name

    # Send file back to user
    response = send_file(tmp_path, as_attachment=True, download_name="stock_performance.xlsx")
    @response.call_on_close
    def cleanup():
        os.remove(tmp_path)
    return response

@app.route("/get-gainers-losers", methods=["GET"])
def get_gainers_losers():
    """Fetch top gainers and losers dynamically from NSE."""
    stock_symbols = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
        "SBIN.NS", "BHARTIARTL.NS", "ADANIENT.NS", "JSWSTEEL.NS", "ITC.NS",
        "LT.NS", "KOTAKBANK.NS", "AXISBANK.NS", "HCLTECH.NS", "MARUTI.NS",
        "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS", "BAJFINANCE.NS"
    ]

    stocks_data = []
    for symbol in stock_symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")
            if len(hist) < 2:
                continue
            price = hist["Close"].iloc[-1]
            previous_close = hist["Close"].iloc[-2]
            change = price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close != 0 else 0

            stock_info = stock.info
            logo_url = stock_info.get("logo_url", None)
            if not logo_url or not isinstance(logo_url, str) or not logo_url.startswith("http"):
                website = stock_info.get("website", "")
                if website and website.startswith("http"):
                    domain = website.split("//")[-1].split("/")[0]
                    logo_url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"
                else:
                    logo_url = "/static/images/default.png"

            stocks_data.append({
                "symbol": symbol,
                "name": stock.info.get("shortName", symbol),
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "logo": logo_url,
            })
        except Exception:
            continue

    gainers = sorted([s for s in stocks_data if s["change"] > 0], key=lambda x: x["change_percent"], reverse=True)[:10]
    losers = sorted([s for s in stocks_data if s["change"] < 0], key=lambda x: x["change_percent"])[:10]

    return jsonify({"gainers": gainers, "losers": losers})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/performance")
def performance():
    return render_template("performance.html")

@app.route("/upload", methods=["POST"])
def upload_stock_info():
    """Handle stock information upload."""
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400
    user_input = data.get("stock_symbol")
    if not user_input:
        return jsonify({"message": "Stock symbol is required"}), 400
    stock_symbol = resolve_symbol(user_input)
    exchange = data.get("exchange", "").upper()
    try:
        quantity = int(data.get("quantity"))
        purchase_price = float(data.get("purchase_price"))
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid quantity or purchase price"}), 400

    updated_rows = []
    stock_found = False

    # Check if the stock already exists and update it
    if os.path.exists(STOCK_FILE):
        with open(STOCK_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == stock_symbol and row[1] == exchange:
                    updated_rows.append([stock_symbol, exchange, quantity, purchase_price])
                    stock_found = True
                else:
                    updated_rows.append(row)

    if not stock_found:
        updated_rows.append([stock_symbol, exchange, quantity, purchase_price])

    with open(STOCK_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    if stock_found:
        return jsonify({"message": f"Stock {stock_symbol} updated successfully!"})
    else:
        return jsonify({"message": f"Stock {stock_symbol} added successfully!"})

@app.route("/get-performance", methods=["GET"])
def calculate_stock_performance():
    if not os.path.exists(STOCK_FILE):
        return jsonify({"error": "No stock information found. Please upload stock info first."})

    results = []
    with open(STOCK_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 4:
                continue
            stock_symbol, exchange, quantity, purchase_price = row
            try:
                quantity = int(quantity)
                purchase_price = float(purchase_price)
                actual_price = fetch_actual_price(stock_symbol, exchange)
                # Fetch stock info for name and logo
                stock = yf.Ticker(stock_symbol)
                stock_info = stock.info
                stock_name = stock_info.get("shortName", stock_symbol)
                logo_url = stock_info.get("logo_url", None)
                if not logo_url or not isinstance(logo_url, str) or not logo_url.startswith("http"):
                    website = stock_info.get("website", "")
                    if website and website.startswith("http"):
                        domain = website.split("//")[-1].split("/")[0]
                        logo_url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"
                    else:
                        logo_url = "/static/images/default.png"
                if actual_price is not None:
                    profit_loss = (actual_price - purchase_price) * quantity
                    results.append({
                        "stock_symbol": stock_symbol,
                        "stock_name": stock_name,
                        "logo": logo_url,
                        "exchange": exchange,
                        "quantity": quantity,
                        "purchase_price": purchase_price,
                        "actual_price": actual_price,
                        "profit_loss": profit_loss
                    })
            except Exception:
                continue
    return jsonify(results)

@app.route("/delete-stock", methods=["POST"])
def delete_stock():
    data = request.json
    stock_symbol = data.get("stock_symbol")
    updated_rows = []

    # If file does not exist or is empty, just return success
    if not os.path.exists(STOCK_FILE) or os.path.getsize(STOCK_FILE) == 0:
        return jsonify({"message": f"Stock {stock_symbol} deleted successfully!"})

    with open(STOCK_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            # Only keep rows that do not match the symbol
            if row and row[0] != stock_symbol:
                updated_rows.append(row)

    with open(STOCK_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    return jsonify({"message": f"Stock {stock_symbol} deleted successfully!"})

def fetch_actual_price(stock_symbol, exchange):
    # Try yfinance first
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            return hist["Close"].iloc[-1]
    except Exception as e:
        print(f"yfinance error for {stock_symbol}: {e}")

    # Fallback to nsetools for NSE
    if exchange == "NSE":
        try:
            nse = Nse()
            nse_symbol = stock_symbol.replace(".NS", "").upper()
            q = nse.get_quote(nse_symbol)
            if q and "lastPrice" in q:
                price_str = q["lastPrice"].replace("₹", "").replace(",", "").strip()
                return float(price_str)
        except Exception as e:
            print(f"nsetools error for {stock_symbol}: {e}")
    return None
@app.route("/download-pdf", methods=["GET"])
def download_pdf():
    # Fetch performance data
    if not os.path.exists(STOCK_FILE):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="No stock information found.", ln=True, align="L")
        pdf_file = "performance_report.pdf"
        pdf.output(pdf_file)
        return send_file(pdf_file, as_attachment=True)

    # Get the performance data as in /get-performance
    results = []
    with open(STOCK_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 4:
                continue
            stock_symbol, exchange, quantity, purchase_price = row
            try:
                quantity = int(quantity)
                purchase_price = float(purchase_price)
                actual_price = fetch_actual_price(stock_symbol, exchange)
                stock = yf.Ticker(stock_symbol)
                stock_info = stock.info
                stock_name = stock_info.get("shortName", stock_symbol)
                logo_url = stock_info.get("logo_url", None)
                if not logo_url or not isinstance(logo_url, str) or not logo_url.startswith("http"):
                    website = stock_info.get("website", "")
                    if website and website.startswith("http"):
                        domain = website.split("//")[-1].split("/")[0]
                        logo_url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"
                    else:
                        logo_url = None
                if actual_price is not None:
                    profit_loss = (actual_price - purchase_price) * quantity
                    results.append({
                        "stock_symbol": stock_symbol,
                        "stock_name": stock_name,
                        "logo": logo_url,
                        "exchange": exchange,
                        "quantity": quantity,
                        "purchase_price": purchase_price,
                        "actual_price": actual_price,
                        "profit_loss": profit_loss
                    })
            except Exception:
                continue

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Stock Performance Report", ln=True, align="C")
    pdf.ln(5)

    # Table header
    pdf.set_font("Arial", "B", 10)
    col_widths = [20, 35, 25, 18, 18, 25, 25, 25, 25]
    headers = ["Logo", "Stock Name", "Symbol", "Exch", "Qty", "Buy Price", "Curr Price", "Profit/Loss"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 9)
    for row in results:
        # Logo
        logo_path = None
        if row["logo"]:
            try:
                resp = requests.get(row["logo"], timeout=5)
                if resp.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                        tmp_img.write(resp.content)
                        logo_path = tmp_img.name
            except Exception:
                logo_path = None

        y_before = pdf.get_y()
        x_before = pdf.get_x()
        if logo_path:
            pdf.cell(col_widths[0], 15, "", border=1)
            pdf.image(logo_path, x=x_before+2, y=y_before+2, w=col_widths[0]-4, h=col_widths[0]-4)
        else:
            pdf.cell(col_widths[0], 15, "N/A", border=1, align="C")
        pdf.set_xy(x_before + col_widths[0], y_before)

        # Stock Name
        pdf.cell(col_widths[1], 15, str(row["stock_name"]), border=1)
        # Symbol
        pdf.cell(col_widths[2], 15, str(row["stock_symbol"]), border=1)
        # Exchange
        pdf.cell(col_widths[3], 15, str(row["exchange"]), border=1)
        # Quantity
        pdf.cell(col_widths[4], 15, str(row["quantity"]), border=1)
        # Purchase Price
        pdf.cell(col_widths[5], 15, f"{row['purchase_price']:.2f}", border=1)
        # Current Price
        pdf.cell(col_widths[6], 15, f"{row['actual_price']:.2f}", border=1)
        # Profit/Loss
        pdf.cell(col_widths[7], 15, f"{row['profit_loss']:.2f}", border=1)
        pdf.ln(15)

        # Clean up temp logo file
        if logo_path:
            try:
                os.unlink(logo_path)
            except Exception:
                pass

    pdf_file = "performance_report.pdf"
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

# Expose the app as 'application' for Gunicorn/Render compatibility
application = app

if __name__ == "__main__":
    app.run(debug=True)