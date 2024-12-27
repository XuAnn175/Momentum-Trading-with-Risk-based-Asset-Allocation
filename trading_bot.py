import hmac
import hashlib
import datetime
import requests
import time
from utils import get_POST_headers
from order import Order

class TradingBot:
    def __init__(self,symbol):
        self.symbol = symbol
        self.staging_api_secret_key = 'VZAEUXGFGW7YMKVFNUHEJDV5NYV6'
        self.staging_api_key = 'mDJ2OALU0SfsmQU8aJxlOw=='
            
    def send_order(self, **kwargs):
        # Create order object
        order = Order(**kwargs)
        
        # Convert order to API format
        data = order.to_dict()
        
        # Send request
        headers = get_POST_headers(self.staging_api_key, self.staging_api_secret_key, data)
        response = requests.post('https://api.staging.woo.org/v1/order', headers=headers, data=data)
        print(response.status_code)
        return response.json()

    def cancel_order(self, order_id: int, symbol: str):
        data = {
            'order_id': order_id,
            'symbol': symbol
        }
        
        headers = get_POST_headers(self.staging_api_key, self.staging_api_secret_key, data)
        response = self.session.delete(
            'https://api.staging.woox.io/v1/order',
            data=data,
            headers=headers
        )
        return response.json()

    def get_available_balance(self):
        data = {
            'symbol': self.symbol
        }
        headers = get_POST_headers(self.staging_api_key, self.staging_api_secret_key, data)
        response = self.session.get('https://api.staging.woox.io/v1/account', headers=headers)
        return response.json()
    
if __name__ == "__main__":
    bot = TradingBot('SPOT_BTC_USDT')

    response = bot.send_order(
        symbol='SPOT_BTC_USDT',
        order_type='MARKET',
        side='BUY',
        order_quantity=0.00025,
    )
    print(response)

    # response = bot.cancel_order(order_id=4032277924,symbol='SPOT_BTC_USDT')
    # print(response)

