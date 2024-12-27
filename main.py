import asyncio
from data_parser import DataParser

data_parser = DataParser()
symbols = ['SPOT_BTC_USDT']
try:
    asyncio.run(data_parser.start_subscriptions(symbols))
except KeyboardInterrupt:
    print("Shutting down gracefully...")
