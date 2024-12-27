import datetime
import hmac
import hashlib

def generate_signature(staging_api_secret_key, data):
    key = staging_api_secret_key       #'key' # Defined as a simple string.
    key_bytes= bytes(key , 'utf-8')         # Commonly 'latin-1' or 'utf-8'
    data_bytes = bytes(data, 'utf-8')       # Assumes `data` is also a string.
    return hmac.new(key_bytes, data_bytes , hashlib.sha256).hexdigest()

def get_GET_headers(staging_api_key, staging_api_secret_key):
    milliseconds_since_epoch = round(datetime.datetime.now().timestamp() * 1000)
    signature_base = f"|{milliseconds_since_epoch}"
    x_api_signature = generate_signature(staging_api_secret_key, signature_base)
    
    headers = {
        'x-api-timestamp': str(milliseconds_since_epoch),
        'x-api-key': staging_api_key,
        'x-api-signature': x_api_signature,
        'Content-Type': 'application/json',  # Changed to JSON for v3 API
        'Cache-Control': 'no-cache'
    }

    return headers

def get_POST_headers(staging_api_key, staging_api_secret_key, params):
    milliseconds_since_epoch = round(datetime.datetime.now().timestamp() * 1000)
    
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    
    # Generate signature
    signature_base = f"{query_string}|{milliseconds_since_epoch}"
    x_api_signature = generate_signature(staging_api_secret_key, signature_base)
    
    headers = {
        'x-api-timestamp': str(milliseconds_since_epoch),
        'x-api-key': staging_api_key,
        'x-api-signature': x_api_signature,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }
    return headers

class OrderBook:
    def __init__(self, symbol):
        self.symbol = symbol
        self.asks = []  # Stores the ask side (price, size)
        self.bids = []  # Stores the bid side (price, size)
        self.timestamp = None
        
    def update(self, data, timestamp):
        """Updates the orderbook with new data."""
        if data["symbol"] != self.symbol:
            raise ValueError("Data symbol does not match orderbook symbol")
        
        self.asks = data["asks"]
        self.bids = data["bids"]
        self.timestamp = timestamp

    def dump(self, max_level=10):
        """Prints the orderbook in a vertical format."""
        max_ask_level = min(max_level, len(self.asks))  # Limit ask levels to max_level
        max_bid_level = min(max_level, len(self.bids))  # Limit bid levels to max_level

        print(f"Orderbook for {self.symbol} (Top {max_level} levels):")
        print(f"{'Ask Price':>15} | {'Ask Size':>15}")
        print("-" * 35)

        # Print Ask orders (sorted from highest to lowest)
        ask_prices = []
        ask_sizes = []
        for i in range(max_ask_level):
            ask_price, ask_size = self.asks[i]
            ask_prices.append(ask_price)
            ask_sizes.append(ask_size)
            print(f"{ask_price:>15.2f} | {ask_size:>15.6f}")

        print("-" * 35)
        print(f"{'Bid Price':>15} | {'Bid Size':>15}")
        print("-" * 35)

        # Print Bid orders (sorted from highest to lowest)
        bid_prices = []
        bid_sizes = []
        for i in range(max_bid_level):
            bid_price, bid_size = self.bids[i]
            bid_prices.append(bid_price)
            bid_sizes.append(bid_size)
            print(f"{bid_price:>15.2f} | {bid_size:>15.6f}")

        print("-" * 35)

        return {"timestamp": self.timestamp, "ask_prices": ask_prices, "ask_sizes": ask_sizes, "bid_prices": bid_prices, "bid_sizes": bid_sizes}

import json
import asyncio
import websockets

class BBO:
    def __init__(self, symbol: str):
        """Initialize the BBO structure for a specific symbol."""
        self.symbol = symbol
        self.best_bid = None  # Best bid price
        self.best_bid_size = 0  # Size of the best bid
        self.best_ask = None  # Best ask price
        self.best_ask_size = 0  # Size of the best ask

    def update(self, bid_price: float, bid_size: float, ask_price: float, ask_size: float):
        """Update the BBO with new bid and ask data."""
        if self.best_bid is None or bid_price > self.best_bid:
            self.best_bid = bid_price
            self.best_bid_size = bid_size
        elif bid_price == self.best_bid:
            self.best_bid_size += bid_size  # Aggregate size if bid price is the same

        if self.best_ask is None or ask_price < self.best_ask:
            self.best_ask = ask_price
            self.best_ask_size = ask_size
        elif ask_price == self.best_ask:
            self.best_ask_size += ask_size  # Aggregate size if ask price is the same

    def get_bbo(self):
        """Return the best bid and ask as a dictionary."""
        return {
            "symbol": self.symbol,
            "best_bid": self.best_bid,
            "best_bid_size": self.best_bid_size,
            "best_ask": self.best_ask,
            "best_ask_size": self.best_ask_size
        }

    def __str__(self):
        """String representation of the BBO."""
        return f"{self.symbol} BBO - Best Bid: {self.best_bid} ({self.best_bid_size}), Best Ask: {self.best_ask} ({self.best_ask_size})"