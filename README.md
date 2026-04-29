# Nifty 250 Breakout Scanner 🚀

A high-performance full-stack web application that automatically identifies breakout stock patterns across **NSE Nifty 250** stocks using real-time data from `yfinance`.

## Features

- **6 Pattern Types** detected algorithmically:
  - 📈 Volume Breakout
  - ☕ Cup & Handle
  - 🔲 Channel Breakout (30/45/60-day multi-window)
  - 🔁 Multi-Tap Breakout (5+ distinct peak taps)
  - 📐 Triangle Breakout (true pivot-based)
  - 📉 Downtrend Breakout

- **Global Trend Filters** — only shows stocks that are:
  - Trading above the **50 EMA**
  - In a bullish **Supertrend (10, 2)** phase

- **Smart Volume Analysis** — compares today's volume against both 20-day and 50-day averages, using whichever reveals the stronger surge

- **Conviction Engine** — scores every setup on Volume Surge, Risk:Reward, Bullish Close Strength, and EMA Gap. Only **Medium** and **High** conviction setups shown.

- **Top Pick per Category** — the highest-scored stock in each pattern category is crowned "Top Pick" with a glowing card

- **2 Years of Backtesting Data** — fetches 2 years of daily price history for reliable indicator calculations

- **Interactive Charts** — click any card to expand a full 2-year candlestick chart with pattern overlays and Supertrend line

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · FastAPI · yfinance · pandas · scipy |
| Frontend | React · Vite · Lightweight Charts |
| Indicators | 50 EMA · Supertrend (10,2) · ATR · argrelextrema |

## Setup & Run

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8080
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** and click **Run Market Scan**.

## Project Structure
```
nifty250-breakout-scanner/
├── backend/
│   ├── main.py          # FastAPI app & schemas
│   ├── scanner.py       # Pattern detection & conviction engine
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx      # React dashboard with charts & modals
        └── index.css    # Dark-mode premium design system
```

## Disclaimer

This tool is for **educational and research purposes only**. It does not constitute financial advice. Always do your own due diligence before trading.
