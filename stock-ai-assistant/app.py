from datetime import datetime, timezone
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from ai_service import explain_with_ai
from config import load_config
from data_service import get_stock_data
from formatting import create_multi_summary
from parsing import extract_symbols, get_supported_companies


load_dotenv()


st.set_page_config(
    page_title="Stock Data AI Assistant",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-navy: #08111f;
            --bg-navy-2: #0b1728;
            --panel: rgba(13, 21, 34, 0.78);
            --panel-border: rgba(148, 163, 184, 0.14);
            --text-main: #e5edf8;
            --text-muted: #b8c6db;
            --input-bg: #f8fafc;
            --input-text: #0f172a;
            --accent: #10a37f;
            --accent-2: #0f766e;
        }
        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(59,130,246,0.20), transparent 42%),
                radial-gradient(circle at 88% 10%, rgba(56,189,248,0.14), transparent 38%),
                linear-gradient(180deg, var(--bg-navy) 0%, var(--bg-navy-2) 100%);
            color: var(--text-main);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1320px;
        }
        .hero-card, .guidelines-card {
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 20px;
            box-shadow: 0 16px 38px rgba(2, 6, 23, 0.34);
            backdrop-filter: blur(8px);
        }
        .hero-card {
            padding: 1.15rem 1.35rem;
            margin-bottom: 0.75rem;
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
            letter-spacing: -0.02em;
            color: #f8fbff;
        }
        .hero-subtitle {
            color: var(--text-muted);
            margin: 0;
            font-size: 1.02rem;
        }
        .guidelines-card {
            padding: 1.05rem 1.25rem;
            margin-bottom: 0.95rem;
        }
        .guidelines-title {
            font-weight: 800;
            font-size: 1.22rem;
            margin-bottom: 0.45rem;
            color: #f8fbff;
        }
        .guidelines-list {
            margin: 0.25rem 0 0 1.1rem;
            color: #d7e1f0;
            line-height: 1.7;
            font-size: 1.08rem;
        }
        .guidelines-list code {
            background: rgba(148, 163, 184, 0.16);
            color: #dbeafe;
            border: 1px solid rgba(148, 163, 184, 0.14);
            padding: 0.1rem 0.35rem;
            border-radius: 6px;
        }
        .chat-shell {
            background: transparent;
            border: 0;
            box-shadow: none;
            backdrop-filter: none;
            padding: 0.25rem 0;
            margin-top: 0.55rem;
        }
        .empty-prompt-banner {
            width: min(100%, 1280px);
            margin: 0.2rem auto 0.9rem auto;
            padding: 0.85rem 1rem;
            border-radius: 14px;
            background: rgba(10, 18, 31, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.12);
            color: #dbe7f8;
            text-align: center;
            font-size: 1.05rem;
            line-height: 1.55;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
            animation: fadeSlideIn 240ms ease-out;
        }
        .empty-prompt-banner code {
            background: rgba(16, 163, 127, 0.10);
            color: #8af3d8;
            border: 1px solid rgba(16, 163, 127, 0.20);
            border-radius: 6px;
            padding: 0.08rem 0.32rem;
        }
        @keyframes fadeSlideIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        div[data-testid="stChatMessage"] {
            background: transparent;
            border: 0;
            padding: 0.15rem 0;
            max-width: 100%;
            animation: fadeSlideIn 220ms ease-out;
        }
        div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
            line-height: 1.65;
            font-size: 1rem;
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
            margin-left: 8%;
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
            margin-right: 8%;
        }
        div[data-testid="stChatMessage"] > div {
            border-radius: 18px;
            padding: 0.18rem 0.22rem;
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) > div {
            background: linear-gradient(135deg, #0ea37f, #0f766e);
            border: 1px solid rgba(45, 212, 191, 0.18);
            border-top-right-radius: 10px;
            box-shadow: 0 8px 18px rgba(15, 118, 110, 0.18);
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) > div {
            background: rgba(17, 24, 39, 0.74);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-top-left-radius: 10px;
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) [data-testid="stMarkdownContainer"] {
            color: #e8eef9;
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) pre {
            background: rgba(2, 6, 23, 0.55);
        }
        div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) [data-testid="stMarkdownContainer"] {
            color: #eff6ff;
        }
        div[data-testid="stChatMessage"] img {
            filter: saturate(0.9);
        }
        .chat-meta {
            color: #bfd0e6;
            font-size: 0.84rem;
            margin: 0.18rem 0.2rem 0.45rem 0.2rem;
        }
        div[data-testid="stChatInput"] {
            background: rgba(8, 17, 31, 0.92);
            border-top: 1px solid rgba(148, 163, 184, 0.14);
            backdrop-filter: blur(8px);
        }
        div[data-testid="stChatInput"] > div {
            max-width: 1320px;
            margin: 0 auto;
            padding: 0.55rem 0.9rem 0.7rem 0.9rem;
            width: 100%;
        }
        div[data-testid="stChatInput"] form {
            width: 100% !important;
            max-width: 100% !important;
        }
        div[data-testid="stChatInput"] form > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        div[data-testid="stChatInput"] [data-testid="stChatInputTextArea"],
        div[data-testid="stChatInput"] [data-testid="stChatInputContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 auto !important;
        }
        div[data-testid="stChatInput"] textarea {
            border-radius: 16px !important;
            border: 1px solid rgba(148, 163, 184, 0.24) !important;
            background: rgba(255, 255, 255, 0.96) !important;
            color: var(--input-text) !important;
            caret-color: #0f172a !important;
            box-shadow: 0 8px 20px rgba(2, 6, 23, 0.18);
            padding: 0.9rem 1rem !important;
            width: 100% !important;
            min-height: 58px !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #64748b !important;
            opacity: 1;
        }
        div[data-testid="stChatInput"] textarea:focus {
            border-color: rgba(16,163,127,0.55) !important;
            box-shadow: 0 0 0 3px rgba(16,163,127,0.14) !important;
        }
        div[data-testid="stChatInput"] button {
            border-radius: 12px !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            background: rgba(255, 255, 255, 0.06) !important;
            color: #eaf4ff !important;
            transition: all 140ms ease;
        }
        div[data-testid="stChatInput"] button:hover {
            background: rgba(16, 163, 127, 0.18) !important;
            border-color: rgba(16, 163, 127, 0.35) !important;
        }
        [data-testid="stAlert"] {
            border-radius: 14px;
        }
        div[data-testid="stSpinner"] {
            color: #dbeafe;
        }
        [data-testid="stCaptionContainer"] {
            color: #b8c6db !important;
        }
        @media (max-width: 640px) {
            .hero-title { font-size: 1.55rem; }
            .guidelines-list { font-size: 1rem; }
            .empty-prompt-banner { font-size: 0.95rem; text-align: left; }
            div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
                margin-left: 0;
            }
            div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
                margin-right: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_companies" not in st.session_state:
        st.session_state.show_companies = False


def _toggle_companies() -> None:
    st.session_state.show_companies = not st.session_state.show_companies


def _render_header() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Stock Data AI Assistant</div>
            <p class="hero-subtitle">
                Ask stock questions in natural language and get a beginner-friendly explanation
                based on live market data.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("See Companies", on_click=_toggle_companies, use_container_width=False)

    if st.session_state.show_companies:
        supported = get_supported_companies()
        st.markdown(
            """
            <div class="guidelines-card" style="margin-top: 0.7rem;">
                <div class="guidelines-title">Supported Companies (Top 50 USA + Top 50 India)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### USA (50)")
            st.markdown(
                "\n".join(
                    f"{item['rank']}. `{item['ticker']}` - {item['name']}"
                    for item in supported["USA"]
                )
            )
        with col2:
            st.markdown("### India (50)")
            st.markdown(
                "\n".join(
                    f"{item['rank']}. `{item['ticker']}` - {item['name']}"
                    for item in supported["India"]
                )
            )
    st.markdown(
        """
        <div class="guidelines-card">
            <div class="guidelines-title">Prompt Guidelines</div>
            <ul class="guidelines-list">
                <li>Include a ticker or company name, for example <code>AAPL</code>, <code>TSLA</code>, or <code>Microsoft</code>.</li>
                <li>Ask specific questions like price, daily move, comparison, or a plain-English explanation.</li>
                <li>You can compare multiple companies in one prompt (for example: Apple vs Microsoft).</li>
                <li>Responses are for learning only and are not financial advice.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_chat() -> None:
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="empty-prompt-banner">
                Ask a question to begin. Try:
                Compare <code>AAPL</code> and <code>MSFT</code> based on today's price movement,
                and explain it in simple language.
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.chat_message("assistant", avatar=":material/assistant:"):
            st.markdown(
                "I can explain price moves, compare stocks, and summarize the numbers in beginner-friendly language."
            )
    else:
        for msg in st.session_state.messages:
            avatar = ":material/person:" if msg["role"] == "user" else ":material/assistant:"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                if msg.get("meta"):
                    st.caption(msg["meta"])
    st.markdown("</div>", unsafe_allow_html=True)


def _append_message(role: str, content: str, meta: Optional[str] = None) -> None:
    st.session_state.messages.append({"role": role, "content": content, "meta": meta})


def _handle_question(question: str) -> None:
    _append_message("user", question)

    try:
        config = load_config()
    except ValueError as exc:
        _append_message(
            "assistant",
            (
                f"{exc}\n\nAdd `GIT_ACCESS_TOKEN` or `OPENAI_API_KEY` in your `.env` file, "
                "then refresh the app."
            ),
        )
        return

    symbols = extract_symbols(question)
    if not symbols:
        _append_message(
            "assistant",
            "I couldn't find a stock symbol or company name in your prompt. Try adding a ticker like AAPL, TSLA, or MSFT.",
        )
        return

    stock_items = []
    for symbol in symbols:
        item = get_stock_data(symbol)
        if item:
            stock_items.append(item)

    if not stock_items:
        _append_message(
            "assistant",
            "I couldn't fetch valid stock data for the detected symbols. Please check the ticker names and try again.",
        )
        return

    try:
        answer = explain_with_ai(stock_items, question, config)
        if not answer:
            raise ValueError("Empty AI response")
        meta = f"Symbols used: {', '.join(item.symbol for item in stock_items)}"
    except Exception as exc:
        answer = (
            "I couldn't get an AI explanation right now, so here is the raw stock summary instead:\n\n"
            f"{create_multi_summary(stock_items)}"
        )
        meta = f"Fallback summary shown ({type(exc).__name__})."

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    _append_message("assistant", answer, meta=f"{meta} | Data as of: {timestamp}")


def main() -> None:
    _inject_styles()
    _init_state()
    _render_header()

    _render_chat()

    prompt = st.chat_input(
        "Ask about a stock, compare companies, or request a simple explanation of today's movement (example: Compare Apple and Tesla today and explain the difference in simple terms)",
        key="chat_prompt",
    )
    if prompt:
        cleaned = prompt.strip()
        if cleaned:
            with st.spinner("Fetching stock data and generating response..."):
                _handle_question(cleaned)
            st.rerun()
        else:
            st.warning("Enter a stock-related question to continue.")


if __name__ == "__main__":
    main()
