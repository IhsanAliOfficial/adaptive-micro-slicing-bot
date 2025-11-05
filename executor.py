# executor.py
import math
import time
from utils import compute_realized_vol
import logging
log = logging.getLogger(__name__)

class ExecutionManager:
    def __init__(self, market, config):
        self.market = market
        self.config = config

    def decide_slicing(self, burst_prob, base_amount_usd):
        """
        returns list of (amount) slices (in quote asset units)
        Strategy:
         - if burst_prob low: few larger slices
         - if burst_prob high: many small slices (iceberg)
        """
        if burst_prob < 0.2:
            slices = 3
        elif burst_prob < 0.5:
            slices = 6
        else:
            slices = 12
        base_unit = base_amount_usd / slices
        # For crypto: convert USD into asset roughly via last price
        return [base_unit]*slices

    def usd_to_amount(self, usd, last_price):
        return usd / last_price

    def execute_buy(self, symbol, total_usd, burst_prob):
        # fetch price
        ob = self.market.fetch_orderbook(symbol)
        last = None
        if ob and ob.get("asks"):
            last = ob["asks"][0][0]
        else:
            ticker = self.market.exchange.fetch_ticker(symbol)
            last = ticker.get("last")

        if last is None:
            log.error("no price available")
            return []

        slices_usd = self.decide_slicing(burst_prob, total_usd)
        orders = []
        for s_usd in slices_usd:
            amount = self.usd_to_amount(s_usd, last)
            # price: use slightly passive price to reduce slippage in low burst, or slightly aggressive in high burst
            if burst_prob > 0.5:
                price = last * (1.002)  # small aggressivity
            else:
                price = last * (0.998)
            order = self.market.create_order(symbol, "buy", amount, price, order_type="limit")
            orders.append(order)
            time.sleep(0.2)  # small gap between slices
        return orders
