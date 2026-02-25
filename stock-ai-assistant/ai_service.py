from openai import OpenAI
from config import Config
from formatting import create_multi_summary
from models import StockData


def _build_prompt(stock_data: list[StockData], user_question: str) -> str:
    summary = create_multi_summary(stock_data)
    plural = "these stocks" if len(stock_data) > 1 else "this stock"

    return (
        f'The user asked: "{user_question}"\n\n'
        "Here's the current stock data:\n"
        f"{summary}\n\n"
        "Please provide a clear, beginner-friendly explanation that:\n"
        "1. Directly answers their question\n"
        "2. Explains what the numbers mean\n"
        "3. Uses simple language\n"
        "4. Avoids jargon or explains any necessary terms\n"
        "5. Is encouraging and educational\n"
        f"6. If multiple symbols are included, compare {plural} side by side\n\n"
        "Remember: This is for learning, not financial advice."
    )


def explain_with_ai(
    stock_data: list[StockData],
    user_question: str,
    config: Config,
    history: list[dict[str, str]] | None = None,
) -> str:
    client = OpenAI(
        api_key=config.api_key,
        base_url=config.base_url or None,
    )

    prompt = _build_prompt(stock_data, user_question)
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are an experienced financial educator. "
                "Use the conversation context to stay consistent, but only use the current stock data provided. "
                "If the user references earlier turns, summarize or compare without inventing new prices or facts. "
                "Avoid direct financial advice; focus on education and explanation."
            ),
        }
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content
