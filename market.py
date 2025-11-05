# market.py
import ccxt
import time
import numpy as np
from config import Config
from utils import safe_float
import logging

log = logging.getLogger(__name__)

class Market:
    def __init__(self):
        ex_class = getattr(ccxt, Config.EXCHANGE_ID)
        self.exchange = ex_class({
            "apiKey": Config.API_KEY,
            "secret": Config.API_SECRET,
            "enableRateLimit": True,
        })
        # Some exchanges need load_markets
        try:
            self.exchange.load_markets()
        except Exception as e:
            log.info("load_markets failed: %s", e)

    def fetch_ohlcv(self, symbol=None, timeframe=None, limit=200):
        symbol = symbol or Config.SYMBOL
        timeframe = timeframe or Config.TIMEFRAME
        return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def fetch_orderbook(self, symbol=None, limit=50):
        symbol = symbol or Config.SYMBOL
        try:
            ob = self.exchange.fetch_order_book(symbol, limit=limit)
            return ob
        except Exception as e:
            log.debug("orderbook not available: %s", e)
            return None

    def create_order(self, symbol, side, amount, price=None, order_type="limit"):
        if Config.PAPER_MODE:
            log.info("PAPER MODE order simulated: %s %s %s @%s", side, amount, symbol, price)
            # simulate order id
            return {"id":"paper-"+str(time.time()), "status":"closed", "filled":amount, "price":price}
        else:
            return self.exchange.create_order(symbol, order_type, side, amount, price)
