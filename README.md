# Pairs Trading System

![Generated spread z-score demonstration](assets/portfolio-preview.png)

Research cointegrated equity pairs, model a hedge-adjusted spread, and route proposed orders only to Alpaca paper trading or dry-run output.

## Workflow

`prices -> cointegration screen -> OLS hedge ratio -> rolling z-score -> bounded entry/exit signals`

```bash
pip install -e . pytest ruff
pairs-trading --left KO --right PEP
pytest && ruff check . && ruff format --check .
```

The research command downloads current historical prices with yfinance. The adapter refuses non-paper endpoints; submissions remain dry-run unless the adapter is explicitly constructed with `dry_run=False` in your own paper-only integration and local Alpaca environment variables are available. Market data may be unavailable; the pure research and payload tests run offline.

## Complete local setup

Use Python 3.12 or later. Create and activate a virtual environment (`python -m venv .venv`; `.venv/Scripts/Activate.ps1` on Windows or `source .venv/bin/activate` elsewhere), then install from the repository root. `pairs-trading --left KO --right PEP` downloads historical adjusted closes from yfinance, tests the relationship, derives the hedge-adjusted spread, and reports the latest bounded signal. Try a longer history only after the basic command succeeds.

## Paper-trading credentials

The research CLI does not submit orders. A custom caller can use `AlpacaPaperAdapter(dry_run=False)` only with the paper URL and a local ignored `.env` containing `ALPACA_API_KEY=`, `ALPACA_SECRET_KEY=`, and optionally `ALPACA_BASE_URL=https://paper-api.alpaca.markets`. The adapter rejects non-paper URLs. Never expose those values in GitHub, Vercel, browser JavaScript, screenshots, or a public repository.

## Troubleshooting and verification

An empty yfinance result means an unavailable symbol, temporary provider failure, or insufficient overlapping history. Cointegration can disappear as market regimes change, so treat a signal as research output rather than a trade instruction. Run `ruff check . && ruff format --check . && pytest` before publishing.

## Limitations and disclaimer

Cointegration can break down and a backtest cannot establish tradability, fill quality, or profitability. This project is intended for educational and research purposes only. It does not provide investment advice, and its outputs should not be used as the sole basis for financial decisions. Historical performance and simulated results do not guarantee future performance.

MIT License. Author: Aarav Shah.
