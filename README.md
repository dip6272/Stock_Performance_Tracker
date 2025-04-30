# StockPulse - Stock Performance Tracker

StockPulse is a web application designed to help you track your stock investments, monitor market trends, and generate professional reports for your portfolio. With a clean and modern interface, StockPulse makes managing your investments simple and efficient.

---

## 🚀 Features

- **Portfolio Management**: Add, update, and delete stocks in your portfolio with ease.
- **Market Insights**: View top gainers and losers in the Indian stock market (NSE) with stock logos and real-time price changes.
- **Performance Overview**: Analyze your portfolio in a detailed table that includes stock logos, names, symbols, exchange, quantity, buy price, current price, and profit/loss.
- **PDF Reporting**: Export your portfolio as a professional PDF report, complete with stock logos and names, matching the table view.
- **Modern UI**: Enjoy a clean, dark-themed interface for seamless tracking and analysis.

---

## 📸 Screenshots

### Main Page (Top Gainers)
The main page displays the top gainers in the Indian stock market, complete with stock logos and real-time price changes.

![Main Page](attachment/main_page.png)

---

### Performance Tab
The performance tab provides a detailed view of your portfolio, including stock details, current performance, and profit/loss calculations.

![Performance Tab](attachment/performance_tab.png)

---

### Downloaded PDF Report
Generate a professional PDF report of your portfolio, including stock logos and names, for easy sharing or record-keeping.

![PDF Report](attachment/pdf_report.png)

---

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

*Replace `VIDEO_ID` with your actual YouTube video ID.*

---

## 💡 Benefits

- **Visual Portfolio**: Instantly see your stock performance with logos and names.
- **Easy Reporting**: Download a PDF report for sharing or record-keeping.
- **Market Insights**: Track top gainers and losers in real time.
- **Simple Management**: Add, update, and delete stocks with ease.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, yfinance, nsetools, FPDF
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: FPDF with dynamic logo embedding

---

## ⚡ Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR-USERNAME/stock-performance-tracker.git
    cd stock-performance-tracker
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```bash
    python app.py
    ```
    Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📂 Project Structure

```
.
├── app.py
├── user_stocks.csv
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── script.js
│       └── performance.js
├── templates/
│   ├── index.html
│   └── performance.html
├── screenshots/
│   ├── main_page.png
│   ├── performance_tab.png
│   └── pdf_report.png
└── README.md
```

---

## 🙏 Credits

- [yfinance](https://github.com/ranaroussi/yfinance)
- [nsetools](https://github.com/vsjha18/nsetools)
- [FPDF](https://pyfpdf.github.io/)

---

## 📧 Contact

For questions or suggestions, open an issue or contact [dippadwal89@gmail.com].

---

*Happy Investing!*