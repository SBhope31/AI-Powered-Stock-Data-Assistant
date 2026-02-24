"""
Stock Data AI Assistant
========================
An AI assistant that helps you understand stock market data.
Uses real stock information and explains it in simple terms.

DISCLAIMER: This is for educational purposes only. Not financial advice.
"""

from datetime import datetime, timezone
from dotenv import load_dotenv

from ai_service import explain_with_ai
from config import load_config
from data_service import get_stock_data
from formatting import create_multi_summary
from parsing import extract_symbols


def _choose_symbols(symbols: list[str]) -> list[str]:
    if len(symbols) <= 1:
        return symbols

    print("\nMultiple symbols detected:")
    print(", ".join(symbols))
    chosen = input(
        "Enter a comma-separated list to use, or press Enter to use all: "
    ).strip()

    if not chosen:
        return symbols

    selected = [s.strip().upper() for s in chosen.split(",") if s.strip()]
    return selected or symbols


def main() -> None:
    load_dotenv()

    try:
        config = load_config()
    except ValueError as exc:
        print(f"[x] {exc}")
        print("Add GIT_ACCESS_TOKEN or OPENAI_API_KEY to your .env file and try again.")
        return

    print("=" * 60)
    print("Stock Data AI Assistant")
    print("=" * 60)
    print()
    print("[!] EDUCATIONAL USE ONLY - NOT FINANCIAL ADVICE")
    print()
    print("Ask me about stocks! Examples:")
    print("  - 'What's the price of AAPL?'")
    print("  - 'How is TSLA doing today?'")
    print("  - 'Tell me about Microsoft stock (MSFT)'")
    print()

    while True:
        print("-" * 60)
        question = input("\nYour question (or 'quit' to exit): ").strip()

        if question.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye! Happy learning!")
            break

        if not question:
            continue

        symbols = extract_symbols(question)
        if not symbols:
            print("\n[?] I couldn't find a stock symbol in your question.")
            print("Please include a ticker symbol (e.g., AAPL, TSLA, MSFT).")
            continue

        selected_symbols = _choose_symbols(symbols)

        print(f"\n[*] Fetching data for: {', '.join(selected_symbols)}")
        stock_items = []
        for symbol in selected_symbols:
            item = get_stock_data(symbol)
            if not item:
                print(f"[x] Couldn't find data for {symbol}.")
                continue
            stock_items.append(item)

        if not stock_items:
            print("Make sure you're using valid stock ticker symbols.")
            continue

        print("\n[*] Analyzing...")
        explanation = None
        try:
            explanation = explain_with_ai(stock_items, question, config)
        except Exception as exc:
            print("\n[x] There was a problem getting an AI explanation.")
            print("This might be a network issue, rate limit, or API key problem.")
            print(f"Technical details: {exc}")
            print("\nShowing raw stock summary instead.")

        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        if explanation:
            print(explanation)
        else:
            print(create_multi_summary(stock_items))
        print("\n" + "=" * 60)
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"\nData as of: {now_utc}")
        print("[!] For educational purposes only")


if __name__ == "__main__":
    main()
