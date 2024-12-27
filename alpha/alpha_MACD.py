import pandas as pd
import numpy as np
from .baseindicator import BaseIndicator

class MACD(BaseIndicator):
    def __init__(self, slow_window=26, fast_window=12, signal_window=9):
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.signal_window = signal_window
        
    def calculate(self, df):
        """Calculate MACD and Signal line"""
        df = df.copy()
        df["slow_ema"] = df["Adj Close"].ewm(span=self.slow_window, min_periods=self.slow_window).mean()
        df["fast_ema"] = df["Adj Close"].ewm(span=self.fast_window, min_periods=self.fast_window).mean()
        df["macd"] = df["fast_ema"] - df["slow_ema"]
        df["signal"] = df["macd"].ewm(span=self.signal_window, min_periods=self.signal_window).mean()
        return df[["macd", "signal"]]