import asyncio
from data_parser import DataParser
from strategy_backtest import Strategy
import pandas as pd
from trading_bot import TradingBot
import random
from gm_strategy import GMPositionSizer
from account_manager import AccountManager

class OnlineStrategy:
    def __init__(self, symbol):
        self.symbol = symbol
        self.strategy = Strategy()
        self.data_parser = DataParser()
        self.prev_signal = ""
        self.running = True
        self.bot = TradingBot('SPOT_BTC_USDT')
        # Initialize position sizer
        self.position_sizer = GMPositionSizer(
            symbol='SPOT_BTC_USDT',
            history_length=10,
            mu=0.6,
            trading_options=[0.01, 0.02, 0.03, 0.04, 0.05],
            min_balance=0
        )
        self.position_sizer.load_init_data(self.data_parser.klines[self.symbol].ohlcv[-10:])
        self.account_manager = AccountManager()

    def send_order(self, signal, type, current_price):
        available_balance = self.account_manager.get_available_balance() 
        position = self.position_sizer.get_optimal_position_size(
            signal="buy" if signal == 'long' else "sell",
            current_price=current_price,
            available_balance=available_balance,
        )       
        # Get optimal position size
        if type == 'open':
            # if position:
            if signal == 'long':
                self.bot.send_order(
                    symbol='SPOT_BTC_USDT',
                    order_type='MARKET',
                    side='BUY',
                    order_quantity=position['amount'] if position else 0.001
                )
                self.account_manager.position['long'] += position['amount']
                print(f"long open : {position['amount']}")
            else:
                self.bot.send_order(
                    symbol='SPOT_BTC_USDT',
                    order_type='MARKET',
                    side='SELL',
                    order_quantity=position['amount'] if position else 0.001
                )
                self.account_manager.position['short'] += position['amount']
                print(f"short open : {position['amount']}")
        else:
            if signal == 'short': # close short position
                self.bot.send_order(
                    symbol='SPOT_BTC_USDT',
                    order_type='MARKET',
                    side='BUY',
                    order_quantity=self.account_manager.position['short'] 
                )
                self.account_manager.position['short'] = 0
                print(f"short close : {self.account_manager.position['short']}")
            else: # close long position
                self.bot.send_order(
                    symbol='SPOT_BTC_USDT',
                    order_type='MARKET',
                    side='SELL',
                    order_quantity=self.account_manager.position['long']
                )
                self.account_manager.position['long'] = 0   
                print(f"long close : {self.account_manager.position['long']}")

    async def run(self):
        try:
            # await self.data_parser.connect()
            # Create two tasks to run concurrently
            parser_task = asyncio.create_task(self.data_parser.subscribe(self.symbol))
            strategy_task = asyncio.create_task(self.run_strategy())
            
            # Wait for both tasks
            await asyncio.gather(parser_task, strategy_task)
        except Exception as e:
            print(f"Error in strategy: {e}")
        finally:
            self.running = False
            await self.data_parser.close_connection()

    async def run_strategy(self):
        """Separate task for strategy execution"""
        while self.running:
            try:
                kline = self.data_parser.klines.get(self.symbol)
                if kline and len(kline.ohlcv) >= 26:
                    current_df = kline.ohlcv.copy()
                    signal = self.strategy.on_ticks(current_df)
                    print(f"Signal: {signal}")
                    print(current_df[-5:])
                    if signal != self.prev_signal:
                        print(f"New signal generated: {signal} at {current_df.iloc[-1]['Datetime']}")
                        print(f"Current price: {current_df.iloc[-1]['Adj Close']}")
                        
                        self.strategy.hist_prices.append(current_df.iloc[-1]['Adj Close'])
                        
                        # Process signal changes
                        if signal == "" and self.prev_signal == "buy":
                            self.strategy.hist_signals.append("sell")
                            self.send_order("long","close",current_df.iloc[-1]['Adj Close'])
                        elif signal == "" and self.prev_signal == "sell":
                            self.strategy.hist_signals.append("buy")
                            self.send_order("short","close",current_df.iloc[-1]['Adj Close'])
                        elif signal == "" and self.prev_signal == "":
                            self.strategy.hist_signals.append("")
                        elif signal == "buy" and self.prev_signal == "buy":
                            self.strategy.hist_signals.append("")
                        elif signal == "buy" and self.prev_signal == "":
                            self.strategy.hist_signals.append("buy")
                            self.send_order("long","open",current_df.iloc[-1]['Adj Close'])
                        elif signal == "buy" and self.prev_signal == "sell":
                            self.strategy.hist_signals.append("buy")
                            self.send_order("short","close",current_df.iloc[-1]['Adj Close'])
                            self.send_order("long","open",current_df.iloc[-1]['Adj Close'])
                        elif signal == "sell" and self.prev_signal == "sell":
                            self.strategy.hist_signals.append("")
                        elif signal == "sell" and self.prev_signal == "buy":
                            self.strategy.hist_signals.append("sell")
                            self.send_order("long","close",current_df.iloc[-1]['Adj Close'])
                            self.send_order("short","open",current_df.iloc[-1]['Adj Close'])
                        else:
                            self.strategy.hist_signals.append("sell")
                            self.send_order("short","open",current_df.iloc[-1]['Adj Close'])
                        self.prev_signal = signal
                        
                else:
                    print(kline.ohlcv[-5:])
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Error in strategy execution: {e}")

if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    symbol = 'SPOT_BTC_USDT'
    online_strategy = OnlineStrategy(symbol)
    # print(online_strategy.position_sizer.price_history)
    try:
        asyncio.run(online_strategy.run())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")