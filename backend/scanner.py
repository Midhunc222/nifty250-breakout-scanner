import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from typing import List, Dict, Any

NIFTY_250_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "LT.NS",
    "AXISBANK.NS", "ASIANPAINT.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS",
    "TITAN.NS", "BAJAJFINSV.NS", "ULTRACEMCO.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "ADANIENT.NS", "POWERGRID.NS", "NTPC.NS", "WIPRO.NS", "M&M.NS", "LTIM.NS",
    "NESTLEIND.NS", "TECHM.NS", "ONGC.NS", "GRASIM.NS", "HINDALCO.NS", "JSWSTEEL.NS",
    "INDUSINDBK.NS", "DRREDDY.NS", "ADANIPORTS.NS", "CIPLA.NS", "SBILIFE.NS",
    "BAJAJ-AUTO.NS", "EICHERMOT.NS", "BRITANNIA.NS", "TATACHEM.NS", "TVSMOTOR.NS",
    "INDIGO.NS", "HAL.NS", "BEL.NS", "ZOMATO.NS", "JINDALSTEL.NS",
    "TRENT.NS", "CHOLAFIN.NS", "SRF.NS", "HAVELLS.NS", "PIIND.NS", "AUBANK.NS",
    "BANKBARODA.NS", "PNB.NS", "CANBK.NS", "UNIONBANK.NS", "IDFCFIRSTB.NS",
    "SUZLON.NS", "IREDA.NS", "NHPC.NS", "RVNL.NS", "IRFC.NS", "BSE.NS", "CDSL.NS",
    "MCX.NS", "CAMS.NS", "ASHOKLEY.NS", "REC.NS", "PFC.NS",
    "AARTIIND.NS", "ABBOTINDIA.NS", "ACC.NS", "ADANIGREEN.NS", "ALKEM.NS", "APOLLOHOSP.NS",
    "ASTRAL.NS", "ATUL.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BATAINDIA.NS",
    "BERGEPAINT.NS", "BIOCON.NS", "BOSCHLTD.NS", "CASTROLIND.NS", "CGPOWER.NS", "CHAMBLFERT.NS",
    "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", "CUMMINSIND.NS", "DABUR.NS",
    "DALBHARAT.NS", "DEEPAKNTR.NS", "DIVISLAB.NS", "DIXON.NS", "ESCORTS.NS", "EXIDEIND.NS",
    "FEDERALBNK.NS", "FORTIS.NS", "GAIL.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS",
    "GODREJPROP.NS", "GUJGASLTD.NS", "HDFCAMC.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDPETRO.NS",
    "ICICIGI.NS", "ICICIPRULI.NS", "IGL.NS", "INDIAMART.NS", "INDUSTOWER.NS", "IOC.NS",
    "JKCEMENT.NS", "JUBLFOOD.NS", "KAJARIACER.NS", "KANSAINER.NS", "KEI.NS",
    "LALPATHLAB.NS", "LAURUSLABS.NS", "LICHSGFIN.NS", "LUPIN.NS", "MANAPPURAM.NS",
    "MARICO.NS", "MFSL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS",
    "MUTHOOTFIN.NS", "NAVINFLUOR.NS", "NMDC.NS", "OFSS.NS", "OIL.NS",
    "PAGEIND.NS", "PERSISTENT.NS", "PETRONET.NS", "POLYCAB.NS", "RAIN.NS",
    "RAMCOCEM.NS", "SAIL.NS", "SHREECEM.NS", "SIEMENS.NS", "SONACOMS.NS",
    "TATACOMM.NS", "TATACONSUM.NS", "TATAPOWER.NS", "TORNTPHARM.NS", "TORNTPOWER.NS",
    "TRIDENT.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "ZEEL.NS", "ZYDUSLIFE.NS",
    "APLAPOLLO.NS", "ATGL.NS", "ANGELONE.NS", "ANANTRAJ.NS", "APTUS.NS",
    "CAMPUS.NS", "CARTRADE.NS", "CHALET.NS", "CLEAN.NS", "EASEMYTRIP.NS",
    "FINEORG.NS", "GLAXO.NS", "HAPPSTMNDS.NS", "HSCL.NS", "IDFC.NS",
    "IFCI.NS", "IPCALAB.NS", "JBCHEPHARM.NS", "JSWENERGY.NS", "KAYNES.NS",
    "KPITTECH.NS", "LATENTVIEW.NS", "NAUKRI.NS", "NUVAMA.NS", "NYKAA.NS",
    "OLECTRA.NS", "POLICYBZR.NS", "RRKABEL.NS", "SAPPHIRE.NS", "SCHAEFFLER.NS",
    "SOLARINDS.NS", "STLTECH.NS", "SUNTV.NS", "TANLA.NS", "TEJASNET.NS",
    "TTML.NS", "UCOBANK.NS", "UTIAMC.NS", "VEDL.NS", "WELCORP.NS",
]


def fetch_stock_data(symbol: str, period: str = "2y") -> pd.DataFrame:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return None
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def calculate_supertrend(df: pd.DataFrame, period=10, multiplier=2) -> pd.DataFrame:
    df = df.copy()
    hl2 = (df['High'] + df['Low']) / 2
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / period, adjust=False).mean()
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = np.zeros(len(df))
    in_uptrend = np.ones(len(df), dtype=bool)
    supertrend[0] = upperband.iloc[0]

    for i in range(1, len(df)):
        if df['Close'].iloc[i] > upperband.iloc[i - 1]:
            in_uptrend[i] = True
        elif df['Close'].iloc[i] < lowerband.iloc[i - 1]:
            in_uptrend[i] = False
        else:
            in_uptrend[i] = in_uptrend[i - 1]
            if in_uptrend[i] and lowerband.iloc[i] < lowerband.iloc[i - 1]:
                lowerband.iloc[i] = lowerband.iloc[i - 1]
            if not in_uptrend[i] and upperband.iloc[i] > upperband.iloc[i - 1]:
                upperband.iloc[i] = upperband.iloc[i - 1]
        if in_uptrend[i]:
            supertrend[i] = lowerband.iloc[i]
        else:
            supertrend[i] = upperband.iloc[i]

    df['Supertrend'] = supertrend
    df['InUptrend'] = in_uptrend
    return df


def best_volume_multiplier(df: pd.DataFrame) -> tuple:
    """
    Compare today's volume against both 20-day and 50-day averages.
    Returns (multiplier, label) for whichever shows the stronger surge.
    A higher multiplier vs. the 50-day avg is more significant because it
    uses a longer baseline — use that when it beats the 20-day reading.
    """
    recent_vol = float(df.iloc[-1]['Volume'])
    avg20 = df.iloc[-21:-1]['Volume'].mean() if len(df) >= 21 else None
    avg50 = df.iloc[-51:-1]['Volume'].mean() if len(df) >= 51 else None

    m20 = recent_vol / avg20 if avg20 and avg20 > 0 else 0
    m50 = recent_vol / avg50 if avg50 and avg50 > 0 else 0

    # If 50-day multiplier is stronger (stock is surging relative to its
    # longer baseline), prefer that — it's a more convincing signal.
    if m50 >= m20:
        return round(m50, 2), "50d avg"
    return round(m20, 2), "20d avg"


def calc_conviction(df: pd.DataFrame, entry: float, sl: float, target: float,
                    vol_multiplier: float, vol_label: str = "20d avg") -> Dict:
    """Score the quality of a setup and return conviction level + reason."""
    score = 0
    reasons = []

    # 1. Volume surge scoring (vs. whichever baseline was stronger)
    if vol_multiplier >= 3.0:
        score += 40
        reasons.append(f"massive {vol_multiplier:.1f}x surge vs {vol_label}")
    elif vol_multiplier >= 2.0:
        score += 25
        reasons.append(f"strong {vol_multiplier:.1f}x surge vs {vol_label}")
    elif vol_multiplier >= 1.5:
        score += 10
        reasons.append(f"above-average volume ({vol_multiplier:.1f}x vs {vol_label})")

    # 2. Risk-to-Reward scoring
    risk = entry - sl
    reward = target - entry
    rr = reward / risk if risk > 0 else 0
    if rr >= 3.0:
        score += 30
        reasons.append(f"excellent R:R of 1:{rr:.1f}")
    elif rr >= 2.0:
        score += 20
        reasons.append(f"good R:R of 1:{rr:.1f}")
    elif rr >= 1.5:
        score += 10
        reasons.append(f"decent R:R of 1:{rr:.1f}")

    # 3. Strong bullish close (close near top of candle)
    recent = df.iloc[-1]
    candle_range = recent['High'] - recent['Low']
    if candle_range > 0:
        close_strength = (recent['Close'] - recent['Low']) / candle_range
        if close_strength >= 0.85:
            score += 20
            reasons.append("strong bullish close near day high")
        elif close_strength >= 0.70:
            score += 10
            reasons.append("bullish close")

    # 4. EMA buffer: How far above the 50 EMA?
    ema_gap = (recent['Close'] - recent['EMA_50']) / recent['EMA_50'] * 100
    if ema_gap >= 5:
        score += 10
        reasons.append(f"price {ema_gap:.1f}% above 50 EMA")

    if score >= 70:
        conviction = "High"
    elif score >= 40:
        conviction = "Medium"
    else:
        conviction = "Low"

    reason = " | ".join(reasons) if reasons else "Standard breakout setup"
    return {"conviction": conviction, "score": score, "reason": reason}


def check_volume_breakout(df: pd.DataFrame):
    if len(df) < 21: return None
    recent = df.iloc[-1]
    prev_20 = df.iloc[-21:-1]
    recent_high = prev_20['High'].max()

    # Use best-of-20d/50d volume comparison
    vol_multiplier, vol_label = best_volume_multiplier(df)
    vol_surge = vol_multiplier >= 1.8
    bullish = recent['Close'] > recent['Open']
    candle_range = recent['High'] - recent['Low']
    close_near_high = (recent['Close'] - recent['Low']) >= 0.7 * candle_range if candle_range > 0 else False
    breaks_high = recent['Close'] > recent_high

    if vol_surge and bullish and close_near_high and breaks_high:
        entry = float(recent['Close'])
        sl = float(recent['Low'])
        target = entry + 2 * (entry - sl)
        line = [
            {"time": prev_20.index[0].strftime('%Y-%m-%d'), "value": float(recent_high)},
            {"time": recent.name.strftime('%Y-%m-%d'), "value": float(recent_high)}
        ]
        return {
            "name": "Volume Breakout",
            "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
            "hold_time": "1-2 Weeks",
            "vol_multiplier": vol_multiplier,
            "vol_label": vol_label,
            "lines": [{"color": "#06b6d4", "data": line, "lineWidth": 3}]
        }
    return None


def check_cup_and_handle(df: pd.DataFrame):
    if len(df) < 60: return None
    window = df.iloc[-60:]
    max_price = window['High'].max()
    max_idx = window['High'].argmax()
    if max_idx > 40: return None

    recent = df.iloc[-1]
    if recent['Close'] > max_price:
        dip = window.iloc[max_idx:-10]['Low'].min()
        if dip < max_price * 0.85:
            entry = float(recent['Close'])
            sl = float(window.iloc[-10:]['Low'].min())
            target = entry + (max_price - dip)
            avg_vol = df.iloc[-21:-1]['Volume'].mean()
            vol_multiplier = float(recent['Volume']) / avg_vol if avg_vol > 0 else 1.0
            line = [
                {"time": window.index[max_idx].strftime('%Y-%m-%d'), "value": float(max_price)},
                {"time": recent.name.strftime('%Y-%m-%d'), "value": float(max_price)}
            ]
            return {
                "name": "Cup & Handle",
                "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
                "hold_time": "3-4 Weeks",
                "vol_multiplier": round(vol_multiplier, 2),
                "lines": [{"color": "#3b82f6", "data": line, "lineWidth": 3}]
            }
    return None


def check_channel_breakout(df: pd.DataFrame):
    """
    Multi-window channel scanner: tries 30, 45, and 60-day consolidation windows.
    For each window, verifies:
      - Channel height <= 15% (horizontal range)
      - Price visited upper 25% zone at least 2x (resistance touches)
      - Price visited lower 25% zone at least 2x (support touches)
      - Today closes above the upper channel on a bullish candle
    Returns the best (tightest channel) match found across any window.
    """
    if len(df) < 30: return None
    recent = df.iloc[-1]
    best = None  # Track the tightest matching channel

    for window_size in [30, 45, 60]:
        if len(df) < window_size + 1: continue
        window = df.iloc[-(window_size + 1):-1]

        upper_channel = window['High'].max()
        lower_channel = window['Low'].min()
        channel_height = upper_channel - lower_channel
        if lower_channel <= 0: continue

        pct_range = channel_height / lower_channel
        if pct_range > 0.15: continue  # Too wide — not a clean channel

        upper_zone = upper_channel - (channel_height * 0.25)
        lower_zone = lower_channel + (channel_height * 0.25)

        touches_upper = window[window['High'] >= upper_zone]
        touches_lower = window[window['Low'] <= lower_zone]

        if len(touches_upper) < 2 or len(touches_lower) < 2: continue

        if recent['Close'] > upper_channel and recent['Close'] > recent['Open']:
            # Found a valid channel — keep the tightest one (smallest pct_range)
            if best is None or pct_range < best['pct_range']:
                best = {
                    'pct_range': pct_range,
                    'upper_channel': upper_channel,
                    'lower_channel': lower_channel,
                    'channel_height': channel_height,
                    'window': window,
                    'window_size': window_size,
                }

    if best is None: return None

    upper_channel = best['upper_channel']
    lower_channel = best['lower_channel']
    channel_height = best['channel_height']
    window = best['window']

    entry = float(recent['Close'])
    sl = float(lower_channel + (channel_height / 2))
    target = entry + (channel_height * 1.5)
    vol_multiplier, vol_label = best_volume_multiplier(df)

    res_line = [
        {"time": window.index[0].strftime('%Y-%m-%d'), "value": float(upper_channel)},
        {"time": recent.name.strftime('%Y-%m-%d'), "value": float(upper_channel)}
    ]
    sup_line = [
        {"time": window.index[0].strftime('%Y-%m-%d'), "value": float(lower_channel)},
        {"time": recent.name.strftime('%Y-%m-%d'), "value": float(lower_channel)}
    ]
    return {
        "name": f"Channel Breakout ({best['window_size']}d)",
        "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
        "hold_time": "2-3 Weeks",
        "vol_multiplier": vol_multiplier,
        "vol_label": vol_label,
        "lines": [
            {"color": "#ef4444", "data": res_line, "lineWidth": 3},
            {"color": "#10b981", "data": sup_line, "lineWidth": 3}
        ]
    }


def check_multi_tap_breakout(df: pd.DataFrame):
    """
    True Multi-Tap: Uses argrelextrema to find distinct swing-high peaks.
    Requires a minimum of 5 distinct peaks within 3% of the 60-day resistance,
    followed by a clean bullish close above that resistance today.
    """
    if len(df) < 60: return None
    window = df.iloc[-60:-1]
    recent = df.iloc[-1]

    resistance = window['High'].max()
    tap_zone_lower = resistance * 0.97  # Within 3% of resistance

    # Find distinct swing high peaks (order=2 to catch tighter peaks over 60 days)
    peak_indices = argrelextrema(window['High'].values, np.greater, order=2)[0]

    # Count how many peaks reached the tap zone
    tap_count = sum(1 for idx in peak_indices if window['High'].iloc[idx] >= tap_zone_lower)

    # Require a minimum of 5 distinct peak taps
    if tap_count < 5: return None

    if recent['Close'] > resistance and recent['Close'] > recent['Open']:
        avg_vol = df.iloc[-21:-1]['Volume'].mean()
        vol_multiplier = float(recent['Volume']) / avg_vol if avg_vol > 0 else 1.0

        entry = float(recent['Close'])
        sl = float(resistance * 0.95)
        target = entry + (entry - sl) * 2.5

        res_line = [
            {"time": window.index[0].strftime('%Y-%m-%d'), "value": float(resistance)},
            {"time": recent.name.strftime('%Y-%m-%d'), "value": float(resistance)}
        ]

        return {
            "name": f"Multi-Tap ({tap_count} taps)",
            "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
            "hold_time": "1-3 Weeks",
            "vol_multiplier": round(vol_multiplier, 2),
            "lines": [{"color": "#f59e0b", "data": res_line, "lineWidth": 3}]
        }
    return None


def check_triangle_breakout(df: pd.DataFrame):
    if len(df) < 60: return None
    window = df.iloc[-60:-1]
    recent = df.iloc[-1]

    local_max = argrelextrema(window['High'].values, np.greater, order=5)[0]
    local_min = argrelextrema(window['Low'].values, np.less, order=5)[0]

    if len(local_max) < 2 or len(local_min) < 2: return None

    high_idx_1, high_idx_2 = local_max[-2], local_max[-1]
    low_idx_1, low_idx_2 = local_min[-2], local_min[-1]

    high_val_1 = window['High'].iloc[high_idx_1]
    high_val_2 = window['High'].iloc[high_idx_2]
    low_val_1 = window['Low'].iloc[low_idx_1]
    low_val_2 = window['Low'].iloc[low_idx_2]

    if high_val_2 >= high_val_1 or low_val_2 <= low_val_1: return None

    x1, x2 = high_idx_1, high_idx_2
    y1, y2 = high_val_1, high_val_2
    m_high = (y2 - y1) / (x2 - x1)
    resistance_today = m_high * (len(window) - x1) + y1

    if recent['Close'] > resistance_today and recent['Close'] > recent['Open']:
        entry = float(recent['Close'])
        sl = float(low_val_2)
        target = entry + (high_val_1 - low_val_1)
        avg_vol = df.iloc[-21:-1]['Volume'].mean()
        vol_multiplier = float(recent['Volume']) / avg_vol if avg_vol > 0 else 1.0

        upper_line = [
            {"time": window.index[high_idx_1].strftime('%Y-%m-%d'), "value": float(high_val_1)},
            {"time": recent.name.strftime('%Y-%m-%d'), "value": float(resistance_today)}
        ]

        lx1, lx2 = low_idx_1, low_idx_2
        ly1, ly2 = low_val_1, low_val_2
        m_low = (ly2 - ly1) / (lx2 - lx1)
        support_today = m_low * (len(window) - lx1) + ly1

        lower_line = [
            {"time": window.index[low_idx_1].strftime('%Y-%m-%d'), "value": float(low_val_1)},
            {"time": recent.name.strftime('%Y-%m-%d'), "value": float(support_today)}
        ]

        return {
            "name": "Triangle Breakout",
            "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
            "hold_time": "2-4 Weeks",
            "vol_multiplier": round(vol_multiplier, 2),
            "lines": [
                {"color": "#8b5cf6", "data": upper_line, "lineWidth": 3},
                {"color": "#8b5cf6", "data": lower_line, "lineWidth": 3}
            ]
        }
    return None


def check_downtrend_breakout(df: pd.DataFrame):
    """Detect a stock breaking out of a long downtrend line."""
    if len(df) < 60: return None
    window = df.iloc[-60:-1]
    recent = df.iloc[-1]

    local_max = argrelextrema(window['High'].values, np.greater, order=5)[0]
    if len(local_max) < 2: return None

    # Take first and last swing high — need a descending trendline
    hi1_idx, hi2_idx = local_max[0], local_max[-1]
    hi1_val = window['High'].iloc[hi1_idx]
    hi2_val = window['High'].iloc[hi2_idx]
    if hi2_val >= hi1_val: return None  # Not a downtrend

    m = (hi2_val - hi1_val) / (hi2_idx - hi1_idx)
    resistance_today = m * (len(window) - hi1_idx) + hi1_val

    if recent['Close'] > resistance_today and recent['Close'] > recent['Open']:
        entry = float(recent['Close'])
        sl = float(window['Low'].iloc[-5:].min())
        target = entry + (hi1_val - window['Low'].min())
        avg_vol = df.iloc[-21:-1]['Volume'].mean()
        vol_multiplier = float(recent['Volume']) / avg_vol if avg_vol > 0 else 1.0

        trend_line = [
            {"time": window.index[hi1_idx].strftime('%Y-%m-%d'), "value": float(hi1_val)},
            {"time": recent.name.strftime('%Y-%m-%d'), "value": float(resistance_today)}
        ]
        return {
            "name": "Downtrend Breakout",
            "entry": round(entry, 2), "sl": round(sl, 2), "target": round(target, 2),
            "hold_time": "3-5 Weeks",
            "vol_multiplier": round(vol_multiplier, 2),
            "lines": [{"color": "#f97316", "data": trend_line, "lineWidth": 3}]
        }
    return None


def get_category(pattern_name: str) -> str:
    """Normalize pattern name into a clean category key."""
    name_lower = pattern_name.lower()
    if "volume" in name_lower:
        return "Volume Breakout"
    if "cup" in name_lower:
        return "Cup & Handle"
    if "channel" in name_lower:
        return "Channel Breakout"
    if "multi" in name_lower or "tap" in name_lower:
        return "Multi-Tap"
    if "triangle" in name_lower:
        return "Triangle Breakout"
    if "downtrend" in name_lower:
        return "Downtrend Breakout"
    return "Other"


def run_scan() -> List[Dict[str, Any]]:
    raw_results = []

    for symbol in NIFTY_250_SYMBOLS:
        df = fetch_stock_data(symbol)
        if df is None or len(df) < 100:
            continue

        # 1. Calculate indicators
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df = calculate_supertrend(df, period=10, multiplier=2)

        recent = df.iloc[-1]

        # 2. Global Filters: above 50 EMA AND in Bullish Supertrend
        if recent['Close'] <= recent['EMA_50']:
            continue
        if not recent['InUptrend']:
            continue

        # 3. Run all pattern checks
        checks = [
            check_volume_breakout(df),
            check_cup_and_handle(df),
            check_channel_breakout(df),
            check_multi_tap_breakout(df),
            check_triangle_breakout(df),
            check_downtrend_breakout(df),
        ]
        valid_patterns = [c for c in checks if c is not None]
        if not valid_patterns:
            continue

        # 4. Build chart data (last 400 candles ≈ 2 years)
        chart_data = []
        for date, row in df.iloc[-400:].iterrows():
            chart_data.append({
                "time": date.strftime('%Y-%m-%d'),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close'])
            })

        # 5. Supertrend line overlay
        supertrend_line = [
            {"time": date.strftime('%Y-%m-%d'), "value": float(row['Supertrend'])}
            for date, row in df.iloc[-400:].iterrows()
            if row['InUptrend']
        ]

        last_close = float(recent['Close'])
        prev_close = float(df.iloc[-2]['Close'])
        change_pct = ((last_close - prev_close) / prev_close) * 100

        # Use the primary (first) pattern for trade plan & conviction scoring
        primary = valid_patterns[0]
        vol_multiplier = primary.get("vol_multiplier", 1.0)
        vol_label = primary.get("vol_label", "20d avg")
        conviction_data = calc_conviction(
            df, primary['entry'], primary['sl'], primary['target'],
            vol_multiplier, vol_label
        )

        # ── Skip Low conviction setups entirely ──────────────────────────────
        if conviction_data['conviction'] == "Low":
            continue

        pattern_lines = primary['lines'] + [
            {"color": "#eab308", "data": supertrend_line, "lineWidth": 2}
        ]

        raw_results.append({
            "symbol": symbol.replace('.NS', ''),
            "category": get_category(primary['name']),
            "patterns": [p['name'] for p in valid_patterns],
            "close": round(last_close, 2),
            "change": round(change_pct, 2),
            "volume": int(recent['Volume']),
            "chart_data": chart_data,
            "entry": primary['entry'],
            "target": primary['target'],
            "sl": primary['sl'],
            "hold_time": primary['hold_time'],
            "lines": pattern_lines,
            "conviction": conviction_data['conviction'],
            "conviction_score": conviction_data['score'],
            "reason": conviction_data['reason'],
            "is_top_pick": False,
        })

    # 6. Select Top Pick per Category (best conviction_score in each group)
    categories = {}
    for stock in raw_results:
        cat = stock['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(stock)

    for cat, stocks in categories.items():
        best = max(stocks, key=lambda s: s['conviction_score'])
        best['is_top_pick'] = True

    # Sort: top picks first, then by conviction score desc
    raw_results.sort(key=lambda s: (not s['is_top_pick'], -s['conviction_score']))

    return raw_results
