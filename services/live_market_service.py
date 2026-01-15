import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# -----------------------------
# Optional yfinance import
# -----------------------------
try:
    import yfinance as yf
except Exception:
    yf = None
    print("⚠️ yfinance not available, fallback mode enabled")

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# -----------------------------
# Live Market Data (Primary)
# -----------------------------
def fetch_nvda_live_data():
    """
    Fetch live NVIDIA market indicators from Finnhub
    Used as REAL-TIME demand signal
    """
    if not FINNHUB_API_KEY:
        return None

    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=NVDA&token={FINNHUB_API_KEY}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "current_price": data.get("c"),
            "change": data.get("d"),
            "percent_change": data.get("dp"),
            "high": data.get("h"),
            "low": data.get("l"),
            "previous_close": data.get("pc")
        }

    except Exception as e:
        print("⚠️ Finnhub fetch error:", e)
        return None

# -----------------------------
# Historical Price (OPTIONAL)
# -----------------------------
def fetch_nvda_historical_price(date_str="2025-12-31"):
    """
    Fetch NVIDIA historical closing price using yfinance
    SAFE fallback if yfinance is unavailable
    """
    # ✅ HARD GUARD
    if yf is None:
        print("⚠️ Historical price unavailable (yfinance disabled)")
        return None

    try:
        nvda = yf.Ticker("NVDA")

        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)

        hist = nvda.history(
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d")
        )

        if hist.empty:
            return None

        return round(hist["Close"].iloc[0], 2)

    except Exception as e:
        print("⚠️ yfinance runtime error:", e)
        return None
