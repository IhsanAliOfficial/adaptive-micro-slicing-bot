# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env in cwd

class Config:
    EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance")
    API_KEY = os.getenv("API_KEY", "")
    API_SECRET = os.getenv("API_SECRET", "")
    SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
    TIMEFRAME = os.getenv("TIMEFRAME", "1m")
    MAX_POSITION_USD = float(os.getenv("MAX_POSITION_USD", 1000))
    MAX_DAILY_LOSS_USD = float(os.getenv("MAX_DAILY_LOSS_USD", 200))
    PAPER_MODE = os.getenv("PAPER_MODE", "true").lower() in ("true","1","yes")
    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 3))
