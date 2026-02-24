import re


_STOPWORDS = {
    "I",
    "A",
    "AN",
    "AND",
    "ARE",
    "AS",
    "AT",
    "BY",
    "FOR",
    "FROM",
    "HOW",
    "IN",
    "IS",
    "IT",
    "OF",
    "ON",
    "OR",
    "THE",
    "TO",
    "WHAT",
    "WHEN",
    "WHERE",
    "WHY",
    "WITH",
    "WAS",
    "WERE",
    "WILL",
    "YOU",
    "YOUR",
    "ABOUT",
    "PRICE",
    "STOCK",
    "STOCKS",
    "TODAY",
    "NOW",
    "TELL",
    "ME",
    "COMPARE",
    "PERFORMANCE",
    "CURRENT",
}

_TICKER_RE = re.compile(r"\b\$?[A-Z]{1,5}\b", re.IGNORECASE)

_COMPANY_MAP = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",
    "hdfc bank": "HDB",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "state bank of india": "SBIN.NS",
    "sbi": "SBIN.NS",
    "icici bank": "IBN",
    "tata consultancy services": "TCS.NS",
    "tcs": "TCS.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "larsen & toubro": "LT.NS",
    "larsen and toubro": "LT.NS",
    "lt": "LT.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",
    "life insurance corporation of india": "LICI.NS",
    "lic": "LICI.NS",
    "infosys": "INFY",
    "maruti suzuki": "MARUTI.NS",
    "axis bank": "AXISBANK.BO",
    "kotak mahindra bank": "KOTAKBANK.NS",
    "kotak bank": "KOTAKBANK.NS",
    "sun pharmaceutical": "SUNPHARMA.NS",
    "sun pharma": "SUNPHARMA.NS",
    "hcl technologies": "HCLTECH.NS",
    "hcl tech": "HCLTECH.NS",
    "adani": "ADANIENT.NS",
    "adani enterprises": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS",
    "adani green": "ADANIGREEN.NS",
    "adani total gas": "ATGL.NS",
    "adani power": "ADANIPOWER.NS",
    "mrf": "MRF.NS",
    "asian paints": "ASIANPAINT.NS",
    "mahindra & mahindra": "M&M.NS",
    "mahindra and mahindra": "M&M.NS",
    "itc": "ITC.NS",
    "ultratech cement": "ULTRACEMCO.NS",
    "titan company": "TITAN.NS",
    "titan": "TITAN.NS",
}


def extract_symbols(text: str) -> list[str]:
    symbols: list[str] = []

    # Company name mapping (lowercase match).
    lowered = text.lower()
    for name, ticker in _COMPANY_MAP.items():
        if name in lowered:
            symbols.append(ticker)

    # Ticker patterns: $AAPL or AAPL (1-5 letters).
    for match in _TICKER_RE.finditer(text):
        raw = match.group(0)
        token = raw[1:] if raw.startswith("$") else raw
        token = token.upper()

        if token in _STOPWORDS:
            continue

        # Ignore single-letter matches from contractions like "what's", "I'm".
        if len(token) == 1:
            prev = text[match.start() - 1] if match.start() > 0 else ""
            if prev in ("'", "’"):
                continue

        symbols.append(token)

    # De-duplicate while preserving order.
    seen = set()
    result = []
    for sym in symbols:
        if sym not in seen:
            result.append(sym)
            seen.add(sym)
    return result
