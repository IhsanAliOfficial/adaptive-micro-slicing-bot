# bot.py
import logging
import time
from config import Config
from market import Market
from predictor import BurstDetector
from executor import ExecutionManager
from utils import now_ts
import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("trading-bot")

def main():
    market = Market()
    detector = BurstDetector()
    executor = ExecutionManager(market, Config)

    symbol = Config.SYMBOL
    poll = Config.POLL_INTERVAL_SECONDS
    base_trade_usd = min(50, Config.MAX_POSITION_USD*0.1)  # example base trade

    log.info("Starting bot in PAPER_MODE=%s on %s", Config.PAPER_MODE, symbol)

    while True:
        try:
            ohlcv = market.fetch_ohlcv(symbol=symbol, timeframe=Config.TIMEFRAME, limit=200)
            # burst probability
            burst_p = detector.burst_probability(ohlcv)
            log.info("Burst probability: %.3f", burst_p)

            # simple signal: if last candle close > previous + threshold => buy signal (demo)
            df = pd.DataFrame(ohlcv, columns=["ts","o","h","l","c","v"])
            if len(df) >= 2:
                last, prev = df["c"].iloc[-1], df["c"].iloc[-2]
                change = (last - prev) / prev
                # tiny breakout condition
                if change > 0.002 and burst_p < 0.8:
                    log.info("Signal: BUY detected (change=%.4f). Executing slices.", change)
                    orders = executor.execute_buy(symbol, total_usd=base_trade_usd, burst_prob=burst_p)
                    log.info("Orders placed: %s", orders)
                else:
                    log.info("No trade signal (change=%.4f).", change)

            time.sleep(poll)
        except KeyboardInterrupt:
            log.info("Stopping by user")
            break
        except Exception as e:
            log.exception("Main loop error: %s", e)
            time.sleep(poll)

if __name__ == "__main__":
    main()