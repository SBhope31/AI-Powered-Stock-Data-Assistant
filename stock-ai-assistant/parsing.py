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
    "VS",
}

# Supports common Yahoo Finance formats like BRK-B, RELIANCE.NS, BAJAJ-AUTO.NS.
_TICKER_RE = re.compile(r"\b\$?[A-Z&]{1,10}(?:[.-][A-Z]{1,10})?\b", re.IGNORECASE)


SUPPORTED_COMPANIES = [
    # USA (Top 50)
    ("USA", 1, "NVIDIA", "NVDA"),
    ("USA", 2, "Apple", "AAPL"),
    ("USA", 3, "Alphabet (Google)", "GOOG"),
    ("USA", 4, "Microsoft", "MSFT"),
    ("USA", 5, "Amazon", "AMZN"),
    ("USA", 6, "Meta Platforms (Facebook)", "META"),
    ("USA", 7, "Broadcom", "AVGO"),
    ("USA", 8, "Tesla", "TSLA"),
    ("USA", 9, "Berkshire Hathaway", "BRK-B"),
    ("USA", 10, "Walmart", "WMT"),
    ("USA", 11, "Eli Lilly", "LLY"),
    ("USA", 12, "JPMorgan Chase", "JPM"),
    ("USA", 13, "Exxon Mobil", "XOM"),
    ("USA", 14, "Johnson & Johnson", "JNJ"),
    ("USA", 15, "Visa", "V"),
    ("USA", 16, "Micron Technology", "MU"),
    ("USA", 17, "Costco", "COST"),
    ("USA", 18, "Mastercard", "MA"),
    ("USA", 19, "Oracle", "ORCL"),
    ("USA", 20, "AbbVie", "ABBV"),
    ("USA", 21, "Home Depot", "HD"),
    ("USA", 22, "Procter & Gamble", "PG"),
    ("USA", 23, "Chevron", "CVX"),
    ("USA", 24, "Bank of America", "BAC"),
    ("USA", 25, "General Electric", "GE"),
    ("USA", 26, "Caterpillar", "CAT"),
    ("USA", 27, "AMD", "AMD"),
    ("USA", 28, "Coca-Cola", "KO"),
    ("USA", 29, "Netflix", "NFLX"),
    ("USA", 30, "Lam Research", "LRCX"),
    ("USA", 31, "Merck", "MRK"),
    ("USA", 32, "Cisco", "CSCO"),
    ("USA", 33, "Palantir", "PLTR"),
    ("USA", 34, "Applied Materials", "AMAT"),
    ("USA", 35, "Philip Morris International", "PM"),
    ("USA", 36, "Goldman Sachs", "GS"),
    ("USA", 37, "Morgan Stanley", "MS"),
    ("USA", 38, "RTX", "RTX"),
    ("USA", 39, "Wells Fargo", "WFC"),
    ("USA", 40, "T-Mobile US", "TMUS"),
    ("USA", 41, "UnitedHealth", "UNH"),
    ("USA", 42, "McDonald", "MCD"),
    ("USA", 43, "GE Vernova", "GEV"),
    ("USA", 44, "Pepsico", "PEP"),
    ("USA", 45, "Intel", "INTC"),
    ("USA", 46, "American Express", "AXP"),
    ("USA", 47, "IBM", "IBM"),
    ("USA", 48, "Verizon", "VZ"),
    ("USA", 49, "Amgen", "AMGN"),
    ("USA", 50, "AT&T", "T"),
    # India (Top 50)
    ("India", 1, "Reliance Industries", "RELIANCE.NS"),
    ("India", 2, "HDFC Bank", "HDB"),
    ("India", 3, "Bharti Airtel", "BHARTIARTL.NS"),
    ("India", 4, "State Bank of India", "SBIN.NS"),
    ("India", 5, "ICICI Bank", "IBN"),
    ("India", 6, "Tata Consultancy Services", "TCS.NS"),
    ("India", 7, "Bajaj Finance", "BAJFINANCE.NS"),
    ("India", 8, "Larsen & Toubro", "LT.NS"),
    ("India", 9, "Life Insurance Corporation of India (LIC)", "LICI.NS"),
    ("India", 10, "Hindustan Unilever", "HINDUNILVR.NS"),
    ("India", 11, "Infosys", "INFY"),
    ("India", 12, "Maruti Suzuki India", "MARUTI.NS"),
    ("India", 13, "Axis Bank", "AXISBANK.BO"),
    ("India", 14, "Kotak Mahindra Bank", "KOTAKBANK.NS"),
    ("India", 15, "Sun Pharmaceutical", "SUNPHARMA.NS"),
    ("India", 16, "Mahindra & Mahindra", "M&M.NS"),
    ("India", 17, "ITC", "ITC.NS"),
    ("India", 18, "UltraTech Cement", "ULTRACEMCO.NS"),
    ("India", 19, "Titan Company", "TITAN.NS"),
    ("India", 20, "NTPC Limited", "NTPC.NS"),
    ("India", 21, "HCL Technologies", "HCLTECH.NS"),
    ("India", 22, "Adani Ports & SEZ", "ADANIPORTS.NS"),
    ("India", 23, "Oil & Natural Gas", "ONGC.NS"),
    ("India", 24, "Bajaj Finserv", "BAJAJFINSV.NS"),
    ("India", 25, "Bharat Electronics", "BEL.NS"),
    ("India", 26, "JSW Steel", "JSWSTEEL.NS"),
    ("India", 27, "Powergrid Corporation of India", "POWERGRID.NS"),
    ("India", 28, "Adani Enterprises", "ADANIENT.NS"),
    ("India", 29, "Adani Power", "ADANIPOWER.NS"),
    ("India", 30, "Bajaj Auto", "BAJAJ-AUTO.NS"),
    ("India", 31, "Vedanta", "VEDL.NS"),
    ("India", 32, "Coal India", "COALINDIA.NS"),
    ("India", 33, "Hindustan Aeronautics", "HAL.NS"),
    ("India", 34, "Tata Steel", "TATASTEEL.NS"),
    ("India", 35, "Nestle India", "NESTLEIND.NS"),
    ("India", 36, "Indian Oil", "IOC.NS"),
    ("India", 37, "Hindustan Zinc", "HINDZINC.NS"),
    ("India", 38, "DMart", "DMART.NS"),
    ("India", 39, "Eternal (Zomato)", "ETERNAL.NS"),
    ("India", 40, "Asian Paints", "ASIANPAINT.NS"),
    ("India", 41, "Eicher Motors", "EICHERMOT.NS"),
    ("India", 42, "Wipro", "WIT"),
    ("India", 43, "SBI Life Insurance", "SBILIFE.NS"),
    ("India", 44, "Hindalco Industries", "HINDALCO.NS"),
    ("India", 45, "Shriram Transport Finance", "SHRIRAMFIN.NS"),
    ("India", 46, "Grasim Industries", "GRASIM.NS"),
    ("India", 47, "InterGlobe Aviation (IndiGo)", "INDIGO.NS"),
    ("India", 48, "TVS Motor", "TVSMOTOR.NS"),
    ("India", 49, "Hyundai Motor India", "HYUNDAI.NS"),
    ("India", 50, "Divis Laboratories", "DIVISLAB.NS"),
]


_COMPANY_MAP = {name.lower(): ticker for _, _, name, ticker in SUPPORTED_COMPANIES}

_ALIASES = {
    # USA aliases
    "google": "GOOG",
    "alphabet": "GOOG",
    "facebook": "META",
    "meta": "META",
    "berkshire": "BRK-B",
    "berkshire hathaway": "BRK-B",
    "jp morgan": "JPM",
    "jpmorgan": "JPM",
    "johnson and johnson": "JNJ",
    "procter and gamble": "PG",
    "p&g": "PG",
    "coke": "KO",
    "mcdonalds": "MCD",
    "mcdonald's": "MCD",
    "att": "T",
    "t mobile": "TMUS",
    # India aliases
    "reliance": "RELIANCE.NS",
    "airtel": "BHARTIARTL.NS",
    "sbi": "SBIN.NS",
    "icici": "IBN",
    "tcs": "TCS.NS",
    "larsen and toubro": "LT.NS",
    "l&t": "LT.NS",
    "lic": "LICI.NS",
    "hul": "HINDUNILVR.NS",
    "maruti suzuki": "MARUTI.NS",
    "sun pharma": "SUNPHARMA.NS",
    "mahindra and mahindra": "M&M.NS",
    "m&m": "M&M.NS",
    "adani ports": "ADANIPORTS.NS",
    "ongc": "ONGC.NS",
    "powergrid": "POWERGRID.NS",
    "zomato": "ETERNAL.NS",
    "nestle": "NESTLEIND.NS",
    "indigo": "INDIGO.NS",
    "divi's laboratories": "DIVISLAB.NS",
    "divis labs": "DIVISLAB.NS",
}

_COMPANY_MAP.update(_ALIASES)


def get_supported_companies() -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {"USA": [], "India": []}
    for country, rank, name, ticker in SUPPORTED_COMPANIES:
        grouped[country].append({"rank": str(rank), "name": name, "ticker": ticker})
    return grouped


def extract_symbols(text: str) -> list[str]:
    symbols: list[str] = []

    lowered = text.lower()
    for name, ticker in _COMPANY_MAP.items():
        if name in lowered:
            symbols.append(ticker)

    for match in _TICKER_RE.finditer(text):
        raw = match.group(0)
        token = raw[1:] if raw.startswith("$") else raw
        token = token.upper()

        if token in _STOPWORDS:
            continue

        if len(token) == 1:
            prev = text[match.start() - 1] if match.start() > 0 else ""
            if prev in ("'", "’"):
                continue

        symbols.append(token)

    seen = set()
    result = []
    for sym in symbols:
        if sym not in seen:
            result.append(sym)
            seen.add(sym)
    return result
