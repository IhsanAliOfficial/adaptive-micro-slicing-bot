# utils.py
import time
import numpy as np
import pandas as pd

def now_ts():
    return int(time.time())

def compute_realized_vol(returns, window=10):
    # returns: series or list of log returns
    r = np.array(returns[-window:])
    if len(r) < 2:
        return 0.0
    return float(np.sqrt(np.mean(r**2)) * np.sqrt(252*24*60))  # annualized-ish approx

def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default
