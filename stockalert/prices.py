from typing import Optional
import yfinance as yf
from .config import log


def fetch_price(ticker: str) -> Optional[float]:
    try:
        data = yf.Ticker(ticker)
        price = getattr(data.fast_info, "last_price", None)
        if price is None or price != price:
            hist = data.history(period="1d")
            if hist.empty:
                return None
            price = float(hist["Close"].iloc[-1])
        return float(price)
    except Exception as exc:
        log.warning("Price fetch failed for %s: %s", ticker, exc)
        return None


def ticker_exists(ticker: str) -> bool:
    return fetch_price(ticker) is not None


def is_triggered(direction: str, threshold: float, price: float) -> bool:
    if direction == "above":
        return price >= threshold
    return price <= threshold
