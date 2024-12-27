class SignalGenerator:
    def __init__(self):
        self.signal = ""
        self.long_entry_price = 0
        self.short_entry_price = 0
        self.profit = 5
        self.prev_signal = ""

    def generate(self, df):
        """Generate trading signals based on indicators"""
        if self.signal == "":
            if (df["High"].iloc[-1] >= df["rollin_max"].iloc[-1] and 
                df["macd"].iloc[-1] > df["signal"].iloc[-1] and 
                df["obv_slope"].iloc[-1] > 0.5):
                # print(f"buy : rollin_max: {df['rollin_max'].iloc[-1]} MACD: {df['macd'].iloc[-1]} Signal: {df['signal'].iloc[-1]} obv_slope: {df['obv_slope'].iloc[-1]}")
                self.long_entry_price = df["Adj Close"].iloc[-1]
                self.signal = "buy"
            elif (df["Low"].iloc[-1] <= df["rollin_min"].iloc[-1] and 
                  df["macd"].iloc[-1] < df["signal"].iloc[-1] and 
                  df["obv_slope"].iloc[-1] < -0.5):
                # print(f"sell : rollin_min: {df['rollin_min'].iloc[-1]} MACD: {df['macd'].iloc[-1]} Signal: {df['signal'].iloc[-1]} obv_slope: {df['obv_slope'].iloc[-1]}")
                self.short_entry_price = df["Adj Close"].iloc[-1]
                self.signal = "sell"
        elif self.signal == "buy":
            # if (df["Low"].iloc[-1] < df["Adj Close"].iloc[-2] - df["ATR"].iloc[-2] and
            #     df["macd"].iloc[-1] < df["signal"].iloc[-1]):
            if df["Adj Close"].iloc[-1] >= self.long_entry_price + self.profit:
                self.signal = ""
            elif (df["Low"].iloc[-1] <= df["rollin_min"].iloc[-1] and 
                  df["macd"].iloc[-1] < df["signal"].iloc[-1] and 
                  df["obv_slope"].iloc[-1] < -0.5):
                # print(f"sell : rollin_min: {df['rollin_min'].iloc[-1]} MACD: {df['macd'].iloc[-1]} Signal: {df['signal'].iloc[-1]} obv_slope: {df['obv_slope'].iloc[-1]}")
                self.signal = "sell"
                self.short_entry_price = df["Adj Close"].iloc[-1]
        elif self.signal == "sell":
            # if (df["High"].iloc[-1] > df["Adj Close"].iloc[-2] + df["ATR"].iloc[-2] and
            #     df["macd"].iloc[-1] < df["signal"].iloc[-1]):
            if df["Adj Close"].iloc[-1] <= self.short_entry_price - self.profit:
                self.signal = ""
            elif (df["High"].iloc[-1] >= df["rollin_max"].iloc[-1] and 
                  df["macd"].iloc[-1] > df["signal"].iloc[-1] and 
                  df["obv_slope"].iloc[-1] > 0.5):
                # print(f"buy : rollin_max: {df['rollin_max'].iloc[-1]} MACD: {df['macd'].iloc[-1]} Signal: {df['signal'].iloc[-1]} obv_slope: {df['obv_slope'].iloc[-1]}")
                self.signal = "buy"
                self.long_entry_price = df["Adj Close"].iloc[-1]
        self.prev_signal = self.signal
        return self.signal