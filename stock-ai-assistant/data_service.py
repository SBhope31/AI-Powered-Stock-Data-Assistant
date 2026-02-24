from typing import Optional
import yfinance as yf
from models import StockData


def _safe_float(value, default=0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _safe_int(value, default=0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def get_stock_data(symbol: str) -> Optional[StockData]:
    try:
        ticker = yf.Ticker(symbol.upper())

        hist = ticker.history(period="1d")
        if hist.empty:
            return None

        current_price = _safe_float(hist["Close"].iloc[-1])

        info = {}
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        previous_close = _safe_float(info.get("previousClose", 0))
        open_price = _safe_float(info.get("open", 0))
        day_high = _safe_float(info.get("dayHigh", 0))
        day_low = _safe_float(info.get("dayLow", 0))
        volume = _safe_int(info.get("volume", 0))
        market_cap = _safe_int(info.get("marketCap", 0))
        week_52_high = _safe_float(info.get("fiftyTwoWeekHigh", 0))
        week_52_low = _safe_float(info.get("fiftyTwoWeekLow", 0))

        if previous_close > 0:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
        else:
            change = 0.0
            change_percent = 0.0

        return StockData(
            symbol=symbol.upper(),
            name=info.get("longName", symbol.upper()),
            current_price=round(current_price, 2),
            previous_close=round(previous_close, 2),
            open_price=round(open_price, 2),
            day_high=round(day_high, 2),
            day_low=round(day_low, 2),
            volume=volume,
            market_cap=market_cap,
            week_52_high=round(week_52_high, 2),
            week_52_low=round(week_52_low, 2),
            change=round(change, 2),
            change_percent=round(change_percent, 2),
        )
    except Exception:
        return None
