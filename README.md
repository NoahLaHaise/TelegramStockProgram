# Telegram Stock Program

A personal stock monitoring system that delivers daily market alerts and AI-powered portfolio analysis directly to Telegram.

---

## Python — Telegram Alerting (`App.py`)

The Python component is the core of the project. It runs on a cron schedule and pushes two types of messages to a Telegram chat: a real-time watchlist snapshot and a daily AI-generated market briefing.

### How it works

`App.py` is the entry point. Each run calls `send_alert()`, which pulls the latest data for every ticker in `WATCHLIST.py` and sends it to Telegram. Twice a day (around market open and close), it also calls `daily_chat()`, which generates a full AI market report and sends that as well.

### Components

**`StockScreener.py`**
Fetches data for each watchlist ticker using `yfinance` (price history, P/E ratio) and pulls technical indicators (RSI, MACD, Bollinger Bands) from the TradingView screener. Formats everything into a plain-text summary per ticker.

**`WATCHLIST.py`**
A simple list of ticker symbols to monitor. Edit this to add or remove stocks.

**`API/TelegramMessenger.py`**
Handles all communication with the Telegram Bot API. Automatically chunks messages longer than 4096 characters to stay within Telegram's limits.

**`API/GeminiAPI.py`**
Wraps Google's Gemini API. Uses Google Search grounding so the model can pull live news alongside the injected indicator data. Supports standard chat and a background deep-research mode.

**`Prompts/PromptBuilder.py`**
Builds the prompt sent to Gemini. The system prompt instructs the model to act as a financial analyst focused on actionable insights, plain-text formatting, and emoji-based sentiment. The user prompt includes the live watchlist snapshot so Gemini has actual indicator data to reason from.

### Setup

1. Create a `.env` file in `Python/` with:
   ```
   TELEGRAM_ENDPOINT=https://api.telegram.org/bot<YOUR_BOT_TOKEN>
   TELEGRAM_CHAT_ID=<YOUR_CHAT_ID>
   GOOGLE_API_KEY=<YOUR_GEMINI_KEY>
   ```

2. Install dependencies into the virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install yfinance finvizfinance tradingview-screener google-genai python-dotenv
   ```

3. Run manually or schedule with cron:
   ```bash
   python Python/App.py
   ```
   Example cron entry to run every 30 minutes during market hours:
   ```
   */30 9-16 * * 1-5 /path/to/env/bin/python /path/to/Python/App.py
   ```

---

## C++ — Data Analysis Engine

A separate interactive CLI tool for deeper single-stock analysis. It downloads historical price data, computes statistical metrics, and fires a Telegram message with the results.

### What it does

Run the compiled binary, enter a ticker symbol, and the engine will:
1. Download historical OHLCV data to a CSV via a Python helper script (`c++/Python/CSV_stockPrices.py`)
2. Parse the CSV and compute:
   - Mean closing price
   - Daily return standard deviation
   - Sharpe ratio (annualized, using a configurable risk-free rate)
3. Send the results to Telegram using a `config.json` file for API credentials

### Build

Requires CMake and a C++17 compiler.

```bash
mkdir build && cd build
cmake ../c++
cmake --build .
./DataAnalysisEngine
```

The Telegram credentials for the C++ side are read from a `config.json` file at the project root.
