import pandas as pd
import matplotlib.pyplot as plt
from alpha.alpha_MACD import MACD
from alpha.alpha_OBV import OBV
from alpha.alpha_ATR import ATR
from alpha.alpha_ResistanceLines import ResistanceLines
from signal_generator import SignalGenerator
from kline import Kline
from data_parser import DataParser
# Import necessary components from online strategy
from gm_strategy import GMPositionSizer
from account_manager import AccountManager
from tqdm import tqdm 

class Strategy:
    def __init__(self):
        self.signal = ""
        # Initialize indicators
        self.macd = MACD()
        self.obv = OBV()
        self.atr = ATR()
        self.resistance = ResistanceLines()
        self.signal_generator = SignalGenerator()
        self.signal = ""
        self.prev_signal = ""
        self.hist_signals = []
        self.hist_prices = []
        self.hist_balance = []

        # Initialize account and positions
        self.balance = 10000  # Starting with $100,000
        self.account_value = []
        self.position = {'long': 0, 'short': 0}

        # Initialize position sizer and account manager
        self.position_sizer = GMPositionSizer(
            symbol='SPOT_BTC_USDT',
            history_length=10,
            mu=0.6,
            trading_options=[0.001, 0.002, 0.003, 0.004, 0.005],
            min_balance=0
        )
        self.account_manager = AccountManager()

    def on_ticks(self, df):
        df[["macd", "signal"]] = self.macd.calculate(df)
        df[["obv", "obv_slope"]] = self.obv.calculate(df)
        df[["ATR"]] = self.atr.calculate(df)
        df[["rollin_max", "rollin_min"]] = self.resistance.calculate(df)
        
        # Generate signal
        self.signal = self.signal_generator.generate(df)
        return self.signal

    def send_order(self, signal, order_type, current_price):
        """
        Simulate sending an order by updating positions and balance.
        """
        available_balance = self.balance
        position = self.position_sizer.get_optimal_position_size(
            signal="buy" if signal == 'long' else "sell",
            current_price=current_price,
            available_balance=available_balance,
        )
        # Get optimal position size
        if order_type == 'open':
            if signal == 'long':
                print(f"{current_price} : long open : {position['action']} : {position['amount']}")
                self.position['long'] += position['amount']
                self.balance -= position['amount'] * current_price
            else:
                print(f"{current_price} : short open : {position['action']} : {position['amount']}")
                self.position['short'] += position['amount']
                self.balance += position['amount'] * current_price
        else:
            if signal == 'short':  # close short position
                print(f"{current_price} : short close : {position['action']} : {position['amount']}")
                self.position['short'] -= position['amount']
                self.balance -= position['amount'] * current_price
            else:  # close long position
                print(f"{current_price} : long close : {position['action']} : {position['amount']}")
                self.position['long'] -= position['amount']
                self.balance += position['amount'] * current_price

    def plot_results(self):
        """Plot all results after backtesting"""
        # Sanity check
        assert len(self.hist_signals) == len(self.hist_prices), "Mismatch between hist_signals and hist_prices lengths."

        # Create figure and axis
        plt.figure(figsize=(15, 7))
        
        # Plot price line
        plt.plot(range(len(self.hist_prices)), self.hist_prices, 
                label='Price', color='blue', alpha=0.6)
        
        # Find indices where signals occurred
        buy_indices = [i for i, signal in enumerate(self.hist_signals) if signal == "buy"]
        sell_indices = [i for i, signal in enumerate(self.hist_signals) if signal == "sell"]
        
        # Plot buy signals
        if buy_indices:
            plt.scatter(buy_indices, 
                    [self.hist_prices[i] for i in buy_indices],
                    color='green', marker='^', s=3, label='Buy')
        
        # Plot sell signals
        if sell_indices:
            plt.scatter(sell_indices, 
                    [self.hist_prices[i] for i in sell_indices],
                    color='red', marker='v', s=3, label='Sell')
        
        # Customize the plot
        plt.title('Trading Signals')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('trading_signals_backtest.png', dpi=300, bbox_inches='tight')
        plt.close()

    def plot_equity_curve(self):
        """Plot the equity curve based on account balance over time"""
        plt.figure(figsize=(15, 7))
        plt.plot(range(len(self.account_value)), 
                 self.account_value, 
                 label='Equity Curve', color='purple')
        plt.title('Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Balance ($)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('equity_curve_backtest.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    pd.options.mode.chained_assignment = None  # default='warn'
    symbol = 'SPOT_BTC_USDT'
    strategy = Strategy()
    df = pd.read_csv('./data/SPOT_BTC_USDT_1m.csv')
    prev_signal = ""
    original_df = df.copy()

    #read the first 10 Adj close price to position_sizer.price_history
    for price in df["Adj Close"].tolist()[:10]:
        strategy.position_sizer.price_history.append(price)
    #use tqdm 

    for i in tqdm(range(10, len(df)), desc = "Backtesting"):
        # Update kline data
        row = df.iloc[i]
        # Simulate updating kline
        # In backtest, we assume data is already sorted
        kline_data = df.iloc[:i+1].copy()

        if len(kline_data) >= 26:
            current_df = kline_data.copy()
            signal = strategy.on_ticks(current_df)
            # print(f"Signal: {signal}")
            print(current_df[-5:])
            if signal != strategy.prev_signal:
                print(f"New signal generated: {signal} at {current_df.iloc[-1]['Datetime']}")
                print(f"Current price: {current_df.iloc[-1]['Adj Close']}")
                
                strategy.hist_prices.append(current_df.iloc[-1]['Adj Close'])
                
                # Process signal changes
                if signal == "" and strategy.prev_signal == "buy":
                    strategy.hist_signals.append("sell")
                    strategy.send_order("long", "close", current_df.iloc[-1]['Adj Close'])
                elif signal == "" and strategy.prev_signal == "sell":
                    strategy.hist_signals.append("buy")
                    strategy.send_order("short", "close", current_df.iloc[-1]['Adj Close'])
                elif signal == "" and strategy.prev_signal == "":
                    strategy.hist_signals.append("")
                elif signal == "buy" and strategy.prev_signal == "buy":
                    strategy.hist_signals.append("")
                elif signal == "buy" and strategy.prev_signal == "":
                    strategy.hist_signals.append("buy")
                    strategy.send_order("long", "open", current_df.iloc[-1]['Adj Close'])
                elif signal == "buy" and strategy.prev_signal == "sell":
                    strategy.hist_signals.append("buy")
                    strategy.send_order("short", "close", current_df.iloc[-1]['Adj Close'])
                    strategy.send_order("long", "open", current_df.iloc[-1]['Adj Close'])
                elif signal == "sell" and strategy.prev_signal == "sell":
                    strategy.hist_signals.append("")
                elif signal == "sell" and strategy.prev_signal == "buy":
                    strategy.hist_signals.append("sell")
                    strategy.send_order("long", "close", current_df.iloc[-1]['Adj Close'])
                    strategy.send_order("short", "open", current_df.iloc[-1]['Adj Close'])
                else:
                    strategy.hist_signals.append("sell")
                    strategy.send_order("short", "open", current_df.iloc[-1]['Adj Close'])
                strategy.prev_signal = signal
                strategy.account_value.append(strategy.balance + strategy.position['long']*current_df.iloc[-1]['Adj Close'] - strategy.position['short']*current_df.iloc[-1]['Adj Close'])
                if i == len(df) - 1:
                    if strategy.prev_signal == "buy":
                        strategy.send_order("long", "close", df.iloc[-1]['Adj Close'])
                        strategy.hist_signals.append("sell")
                        strategy.account_value.append(strategy.balance + strategy.position['long']*df.iloc[-1]['Adj Close'] - strategy.position['short']*df.iloc[-1]['Adj Close'])
                    elif strategy.prev_signal == "sell":
                        strategy.send_order("short", "close", df.iloc[-1]['Adj Close'])
                        strategy.hist_signals.append("buy")
                        strategy.account_value.append(strategy.balance + strategy.position['long']*df.iloc[-1]['Adj Close'] - strategy.position['short']*df.iloc[-1]['Adj Close'])

        else:
            # Not enough data to generate signal
            pass

    # Plot the results
    strategy.plot_results()
    strategy.plot_equity_curve()

    # Print final account balance
    # print(f"Final Balance: ${strategy.account_manager.balance:.2f}")
    # print(f"Final Positions: {strategy.account_manager.position}")