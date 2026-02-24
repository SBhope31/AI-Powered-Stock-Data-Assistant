from models import StockData


def format_large_number(num: int) -> str:
    if num >= 1_000_000_000_000:
        return f"${num/1_000_000_000_000:.2f}T"
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.2f}B"
    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    return f"${num:,.0f}"


def create_stock_summary(data: StockData) -> str:
    return (
        f"Stock: {data.name} ({data.symbol})\n"
        f"Current Price: ${data.current_price}\n"
        f"Change: ${data.change} ({data.change_percent:+.2f}%)\n"
        f"Previous Close: ${data.previous_close}\n\n"
        "Today's Trading:\n"
        f"- Open: ${data.open_price}\n"
        f"- High: ${data.day_high}\n"
        f"- Low: ${data.day_low}\n"
        f"- Volume: {data.volume:,}\n\n"
        "52-Week Range:\n"
        f"- High: ${data.week_52_high}\n"
        f"- Low: ${data.week_52_low}\n\n"
        f"Market Cap: {format_large_number(data.market_cap)}\n"
    )


def create_multi_summary(items: list[StockData]) -> str:
    return "\n\n".join(create_stock_summary(item) for item in items)
