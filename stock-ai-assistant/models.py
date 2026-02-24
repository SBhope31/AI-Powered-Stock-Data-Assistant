from dataclasses import dataclass


@dataclass(frozen=True)
class StockData:
    symbol: str
    name: str
    current_price: float
    previous_close: float
    open_price: float
    day_high: float
    day_low: float
    volume: int
    market_cap: int
    week_52_high: float
    week_52_low: float
    change: float
    change_percent: float
