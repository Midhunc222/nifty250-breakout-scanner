# 🚀 Nifty 250 Breakout Scanner — Local Setup Guide

## Overview

This dashboard scans **Nifty 250 stocks** in real-time for high-conviction breakout patterns using 2 years of historical data. It runs as two local services:

| Service | Technology | Port |
|---|---|---|
| **Backend** (scanner engine) | Python · FastAPI | `8080` |
| **Frontend** (dashboard UI) | React · Vite | `5173` |

---

## Prerequisites

Make sure you have these installed:

- **Python 3.10+** → check: `python3 --version`
- **Node.js 18+** → check: `node --version`
- **npm** → check: `npm --version`

---

## 📁 Project Location

```
/Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/
├── backend/
│   ├── main.py          ← FastAPI app
│   ├── scanner.py       ← All pattern detection logic
│   ├── requirements.txt ← Python dependencies
│   └── venv/            ← Python virtual environment (local only)
└── frontend/
    ├── src/
    │   ├── App.jsx      ← Main dashboard component
    │   └── index.css    ← Premium dark-mode styles
    ├── package.json
    └── vercel.json
```

---

## 🛠️ First-Time Setup (do this once)

### Backend Setup

```bash
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/frontend

# Install Node dependencies
npm install
```

---

## ▶️ Running the Dashboard (every time)

You need **two terminal windows** open simultaneously.

### Terminal 1 — Start the Backend

```bash
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/backend

source venv/bin/activate

uvicorn main:app --port 8080
```

✅ You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8080
```

---

### Terminal 2 — Start the Frontend

```bash
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/frontend

npm run dev
```

✅ You should see:
```
VITE v5.x ready in 300ms
➜  Local:   http://localhost:5173/
```

---

### Terminal 3 (optional) — Quick health check

```bash
curl http://localhost:8080/api/health
# Expected: {"status":"healthy"}
```

---

## 🖥️ Opening the Dashboard

Open your browser and go to:

```
http://localhost:5173
```

Click **"Run Market Scan"** — the scan takes **30–90 seconds** (fetching 2 years of data for 150+ Nifty 250 stocks).

---

## 📊 What the Dashboard Shows

### Global Filters (applied to every stock)
- ✅ Price **above 50 EMA** (macro uptrend only)
- ✅ In **Bullish Supertrend (10, 2)** phase

### Pattern Categories Detected
| Pattern | What it means | Hold Time |
|---|---|---|
| 📈 Volume Breakout | Massive volume surge (1.8x+ avg) breaking 20-day high | 1–2 Weeks |
| ☕ Cup & Handle | U-shaped recovery + handle + breakout | 3–4 Weeks |
| 🔲 Channel Breakout | Price breaks out of a tight horizontal channel | 2–3 Weeks |
| 🔁 Multi-Tap (5+ taps) | Stock rejected from resistance 5+ times, then breaks through | 1–3 Weeks |
| 📐 Triangle Breakout | Converging Lower Highs + Higher Lows → breakout | 2–4 Weeks |
| 📉 Downtrend Breakout | Price smashes through a descending trendline | 3–5 Weeks |

### Conviction Levels
| Level | Score | Criteria |
|---|---|---|
| 🟢 **High** | ≥ 70 | Massive volume + strong R:R + bullish close near day high |
| 🟡 **Medium** | 40–69 | Some combination of volume surge, decent R:R, bullish close |
| *(Low is filtered out)* | < 40 | Not shown on dashboard |

### Trade Plan (per stock)
Every detected breakout shows:
- **Entry** — Current close price to enter
- **Target** — Expected price based on pattern projection
- **Stop Loss** — Maximum loss if pattern fails
- **R:R Ratio** — Risk to Reward ratio
- **Hold Time** — Recommended holding period

### Top Picks
The **highest-conviction stock per category** is shown in a glowing **Top Pick** hero card at the top of the dashboard.

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---|---|
| Backend won't start | Make sure venv is activated: `source venv/bin/activate` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Frontend shows "Failed to fetch" | Ensure backend is running on port 8080 |
| Scan returns 0 results | Market may be closed / no stocks passed the EMA + Supertrend filter today — try next trading day |
| `npm run dev` fails | Run `npm install` in the frontend folder first |

---

## 🔄 Stopping the Services

In each terminal, press **Ctrl + C** to stop.

---

## 📌 Quick Reference Card

```bash
# ── BACKEND ──────────────────────────────────────────
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/backend
source venv/bin/activate
uvicorn main:app --port 8080

# ── FRONTEND (new terminal) ───────────────────────────
cd /Users/midhunchandran/.gemini/antigravity/scratch/nifty250-breakout-scanner/frontend
npm run dev

# ── OPEN IN BROWSER ───────────────────────────────────
open http://localhost:5173
```

---

*Last updated: April 2026 · GitHub: https://github.com/Midhunc222/nifty250-breakout-scanner*
