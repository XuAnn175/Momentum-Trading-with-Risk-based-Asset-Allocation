from utils import get_GET_headers
import requests

class AccountManager:
    def __init__(self):
        self.app_id = '887ddf4a-7e7a-4ea7-982d-8bc75a5f2b17'
        self.uri = f"wss://wss.staging.woox.io/ws/stream/{self.app_id}"
        self.connection = None
        self.staging_api_key = 'mDJ2OALU0SfsmQU8aJxlOw=='
        self.staging_api_secret_key = 'VZAEUXGFGW7YMKVFNUHEJDV5NYV6'
        self.session = requests.Session()
        self.pending_buy_orders = []
        self.pending_sell_orders = []
        self.position = {}
        self.position['long'] = 0
        self.position['short'] = 0
        
    def get_orders(self):
        headers = get_GET_headers(self.staging_api_key, self.staging_api_secret_key)
        response = self.session.get(
            'https://api.staging.woo.org/v1/orders', 
            headers=headers
        )
        return response.json()
    
    def get_holdings(self):
        headers = get_GET_headers(self.staging_api_key, self.staging_api_secret_key)
        response = self.session.get(
            'https://api.staging.woo.org/v1/client/holding', 
            headers=headers
        )
        # for type, holding in response.json()['holding'].items():
        #     print(type, holding)
        return response.json()

    def update_orders(self):
        # Extract order details
        all_orders = self.get_orders()
        for order in all_orders['rows']:
            if order['status'] == 'NEW' and order['side'] == 'BUY':
                self.pending_buy_orders.append(order)
            elif order['status'] == 'NEW' and order['side'] == 'SELL':
                self.pending_sell_orders.append(order)

        return self.pending_buy_orders
    
    def calculate_hourly_PnL(self,datetime):
        pass
    
    def get_available_balance(self):
        response = self.get_holdings()
        return response['holding']['USDT']
    
    def get_available_holdings(self):
        response = self.get_holdings()
        return response['holding']['BTC']
    
if __name__ == '__main__':
    account_manager = AccountManager()
    res = account_manager.get_holdings()
    print(res)
