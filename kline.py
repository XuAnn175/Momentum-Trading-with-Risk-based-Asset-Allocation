import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt

class Kline:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ohlcv = pd.DataFrame(columns=["Datetime","Open", "Adj Close", "Low", "High", "Volume"])

    def update(self, datetime, open, close, low, high, volume):
        """Update data and generate new signals"""
        new_data = pd.DataFrame([{
            # "Datetime": pd.to_datetime(datetime, unit="ms"),
            "Datetime": datetime,
            "Open": open,
            "Adj Close": close,
            "Low": low,
            "High": high,
            "Volume": volume
        }])

        if self.ohlcv.empty or self.ohlcv.iloc[-1]["Open"] != open:
            # print(f"New data received for {self.symbol}: {new_data}")
            self.ohlcv = pd.concat([self.ohlcv, new_data], ignore_index=True)
            # self.ohlcv = self.ohlcv.sort_values(by="Datetime", ascending=True).reset_index(drop=True)
        
        
if __name__ == "__main__":
    pd.options.mode.chained_assignment = None  # default='warn'
    symbol = 'SPOT_BTC_USDT'
    kline = Kline(symbol)
    
    # Read the CSV file once and store it
    df = pd.read_csv('./data/SPOT_BTC_USDT_1m.csv')
    
    for i in range(0, len(df)):
        # print(f"Updating row {i}")
        row = df.iloc[i]
        kline.update(row["Datetime"], row["Open"], row["Adj Close"], 
                    row["Low"], row["High"], row["Volume"])
    
    kline.plot_results()
