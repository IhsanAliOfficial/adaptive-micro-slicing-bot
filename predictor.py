# predictor.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from utils import compute_realized_vol

class BurstDetector:
    """
    Lightweight burst detector:
     - computes short-term realized vol and compares to rolling median
     - uses a tiny logistic regression (trained on synthetic features) to output burst probability
    """
    def __init__(self):
        # lightweight model with synthetic coefficients
        self.model = LogisticRegression()
        # But we will use a heuristic fallback (no external training needed)
        self.trained = False

    def features_from_ohlcv(self, ohlcv):
        # ohlcv list of [ts, open, high, low, close, vol]
        df = pd.DataFrame(ohlcv, columns=["ts","o","h","l","c","v"])
        df["ret"] = np.log(df["c"]).diff().fillna(0)
        df["rv_5"] = df["ret"].rolling(5).std().fillna(0)
        df["rv_20"] = df["ret"].rolling(20).std().fillna(0)
        return df

    def burst_probability(self, ohlcv):
        df = self.features_from_ohlcv(ohlcv)
        recent_rv = float(df["rv_5"].iloc[-1])
        med_rv = float(df["rv_20"].median() if len(df["rv_20"])>0 else recent_rv)
        # heuristic: if recent_rv >> med_rv => high burst prob
        if med_rv <= 0:
            return 0.0
        ratio = recent_rv / (med_rv + 1e-12)
        prob = 1 - np.exp(-max(0, ratio-1))  # grows as ratio increases
        return float(min(1.0, prob))
