# StockPulse - Stock Performance Tracker

StockPulse is a web application to track your stock investments, view top gainers and losers in the Indian stock market, and download a professional PDF report of your portfolio (with stock logos and names).

---

## 🚀 Features

- **Add, update, and delete stocks** in your portfolio.
- **View top gainers and losers** (NSE) with logos and price changes.
- **Performance tab**: See your stocks in a table with logo, name, symbol, exchange, quantity, buy price, current price, and profit/loss.
- **Download PDF report**: Export your portfolio as a PDF, including stock logos and names, matching the table view.
- **Modern UI**: Clean, dark-themed interface for easy tracking.

---

## 📸 Screenshots

### Main Page (Top Gainers)
![Main Page](screenshots/screenshot/mainpage.jpg)

### Performance Tab
![Performance Tab](screenshots/screenshoot/performancepage.jpg)

### Downloaded PDF Report
![PDF Report](screenshots/screenshot/downlodereport.jpg)

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
    ```
    git clone https://github.com/YOUR-USERNAME/stock-performance-tracker.git
    cd stock-performance-tracker
    ```

2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```
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

For questions or suggestions, open an issue or contact [dippadwal89@gmail.com]

---

*Happy Investing!*
