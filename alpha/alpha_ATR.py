import numpy as np
from .baseindicator import BaseIndicator

class ATR(BaseIndicator):
    def __init__(self, window=20):
        self.window = window
        
    def calculate(self, df):
        """Calculate Average True Range"""
        df = df.copy()
        df['H-L'] = abs(df['High'] - df['Low'])
        df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
        df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
        df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1)
        df['ATR'] = df['TR'].rolling(self.window).mean()
        return df[['ATR']]
