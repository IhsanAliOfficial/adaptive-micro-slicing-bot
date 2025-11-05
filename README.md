# adaptive-micro-slicing-bot


Adaptive Micro-Slicing Bot is a lightweight, exchange-agnostic Python prototype that reduces slippage during sudden volatility by combining a **Volatility Burst Detector** with **adaptive micro-slicing (iceberg-style)** order execution. Built with `ccxt` for easy exchange integration, the bot supports **paper mode**, configurable risk limits, and simple ML-lite prediction for short-term burst probability.

**Key features**
- Real-time OHLCV polling and optional orderbook snapshots  
- Volatility Burst Detector (heuristic + ML-lite)  
- Adaptive micro-slicing execution to minimise slippage  
- Paper mode for safe testing (no live orders)  
- Easy to extend for IBKR / MT5 / custom brokers

**Tech stack:** Python 3.9+, ccxt, pandas, numpy, scikit-learn

---

## Quickstart
1. Clone the repo  
   `git clone https://github.com/<your-username>/adaptive-micro-slicing-bot.git`  
2. Create venv & install deps  
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
