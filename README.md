# StockDataGatherAuto
# 📈 StockDataGatherAuto

An automated stock data gathering pipeline that fetches hourly stock market data for specified tickers during market hours, stores it in a CSV, and commits both the data and logs back to this repository — all powered by GitHub Actions.

## 📜 About

**StockDataGatherAuto** is designed to:
- Automatically fetch stock ticker information from the [Webull API](https://www.webull.com/) using a custom Python data-fetcher.
- Run **hourly from 9:30 AM to 3:30 PM ET** (U.S. market hours), plus one final run at **4:00 PM ET**.
- Append new data rows to a central CSV file (`stock_data.csv`) for easy tracking.
- Log all operations to `pipeline.log` with timestamps (using [Loguru](https://github.com/Delgan/loguru)).
- Commit updated CSV and logs back to the repository automatically.

All of this runs **entirely in the cloud** on GitHub’s infrastructure — no need to keep your computer on.

---

## ⚙️ How It Works

### 1. **Data Gathering**
- Implemented in [`GetMeData.py`](GetMeData.py).
- Uses a **thread-safe singleton** to fetch data for specified tickers (`AAPL`, `TSLA` by default) via Webull.
- Supports easy expansion — just add tickers to `return_stocks_to_get_info()`.

### 2. **CSV Handling**
- Implemented in [`CSVHandler.py`](CSVHandler.py).
- Creates a CSV with headers on first run.
- Appends new rows for each ticker on every run.
- Can wipe all rows while preserving the header.
- Can read and print all rows.

### 3. **Logging**
- Implemented in [`main.py`](main.py) using Loguru.
- Logs to `pipeline.log` with 7-day rotation.
- Logs both to file and GitHub Actions console output.

### 4. **Automation**
- Scheduled via `.github/workflows/stock_pipeline.yml`.
- GitHub Actions workflow:
  - Checks out the repo.
  - Installs dependencies from `requirements.txt`.
  - Runs `main.py`.
  - Commits and pushes `stock_data.csv` and `pipeline.log` back to `main` branch.

---

## 🕒 Schedule

The workflow runs automatically at:
- **9:30 AM ET**
- **10:30 AM ET**
- **11:30 AM ET**
- **12:30 PM ET**
- **1:30 PM ET**
- **2:30 PM ET**
- **3:30 PM ET**
- **4:00 PM ET**

Only Monday–Friday, excluding market holidays.

---

## 📂 Project Structure

