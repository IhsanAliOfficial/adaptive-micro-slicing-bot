# Adaptive Micro-Slicing Trading Bot (Prototype)

### What this does
- Polls market data (via ccxt), computes short-term realized volatility and burst probability.
- When a small breakout signal appears, executes **adaptive micro-sliced** orders to reduce slippage.
- Paper mode supported (default via `.env`).

### Files
- `bot.py` — main
- `market.py` — ccxt wrapper
- `predictor.py` — burst detector
- `executor.py` — execution / slicing logic
- `utils.py`, `config.py`
- `.env.example` — rename to `.env` and fill keys

### Run (test)
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. copy `.env.example` -> `.env` (keep PAPER_MODE=true for testing)
4. `python bot.py`

### Notes
- This is a prototype **educational** bot. Test extensively in paper mode before any live usage.
- To connect to other brokers (IBKR, MT5), implement `market.py` methods mapping to their APIs.
