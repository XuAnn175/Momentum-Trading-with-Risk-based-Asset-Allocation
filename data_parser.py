import websockets
import json
from kline import Kline
import asyncio
import ssl
import requests
import csv

class DataParser:
    def __init__(self):
        self.app_id = "887ddf4a-7e7a-4ea7-982d-8bc75a5f2b17"
        self.uri = f"wss://wss.staging.woox.io/ws/stream/{self.app_id}"
        self.connection = None
        self.klines = {}
        self.signal = ""
        self.strategy = None
        self.load_init_data('SPOT_BTC_USDT')

    def load_init_data(self, symbol):
        self.klines[symbol] = Kline(symbol)
        response = self.get_kline(symbol,limit=25)
        for data in response["rows"]:   
            self.klines[symbol].update(data["end_timestamp"], 
                                       data["open"], 
                                       data["close"], 
                                       data["low"], 
                                       data["high"],
                                       data["volume"])
        print("init data loaded", self.klines[symbol].ohlcv[-5:])

    def set_strategy(self, strategy):
        self.strategy = strategy

    async def connect(self):
        """Handles WebSocket connection"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if self.connection is None:
            self.connection = await websockets.connect(self.uri, ssl=ssl_context)
            print(f"Connected to {self.uri}")
        return self.connection
    
    def get_kline(self, symbol, interval="1m", limit = 10):
        endpoint = f'/v1/public/kline'
        params = {
            'symbol': symbol,
            "type": interval,
            'limit': limit,
        }
        response = requests.get('https://api.woox.io' + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def subscribe(self, symbol):
        while True:
            try:
                response = self.get_kline(symbol)
                data = response["rows"][0]
                # print(data)

                self.klines[symbol].update(data["end_timestamp"], 
                                           data["open"], 
                                           data["close"], 
                                           data["low"], 
                                           data["high"],
                                           data["volume"])
            except Exception as e:
                print(f"Error receiving data for {symbol}: {e}")
                await asyncio.sleep(1)

            await asyncio.sleep(1)

    async def respond_pong(self, websocket):
        """Responds to server PINGs with a PONG"""
        pong_message = {
            "event": "pong",
            "ts": int(asyncio.get_event_loop().time() * 1000)  # Current timestamp in milliseconds
        }
        await websocket.send(json.dumps(pong_message))
        print(f"Sent PONG: {pong_message}")

    async def close_connection(self):
        """Gracefully closes the WebSocket connection"""
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
            print("WebSocket connection closed")

    async def start_subscriptions(self, symbols):
        """Start subscriptions for multiple symbols based on the provided config"""
        tasks = [self.subscribe(symbol) for symbol in symbols]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    data_parser = DataParser()
    response = data_parser.get_kline('SPOT_BTC_USDT')
    print(response)
    # asyncio.run(data_parser.subscribe('SPOT_BTC_USDT'))