import datetime

class Order:
    def __init__(self, symbol: str, order_type: str, side: str, 
                 order_price: float = None, order_quantity: float = None,
                 client_order_id: int = 12345, margin_mode: str = 'CROSS',
                 order_tag: str = 'default', order_amount: float = None,
                 reduce_only: bool = False, visible_quantity: float = None,
                 position_side: str = None):
        
        # check required fields
        if not all([symbol, order_type, side]):
            raise ValueError("symbol, order_type, and side are required fields")
        
        # required fields
        self.symbol = symbol
        self.order_type = order_type
        self.side = side
        
        # optional fields
        self.order_price = order_price
        self.order_quantity = order_quantity
        self.client_order_id = client_order_id
        self.margin_mode = margin_mode
        self.order_tag = order_tag
        self.order_amount = order_amount
        self.reduce_only = reduce_only
        self.visible_quantity = visible_quantity
        self.position_side = position_side
        
        # unix time since epoch in milliseconds
        self.local_timestamp = round(datetime.datetime.now().timestamp() * 1000)
        self.estimated_latency = 5

        # Validate order data
        self._validate()
    
    def _validate(self):
        """Validate order parameters based on rules"""
        if self.order_type != 'MARKET' and self.order_price is None:
            raise ValueError("order_price is required for non-MARKET orders")
            
        if not (self.order_type in ['MARKET', 'ASK', 'BID'] and self.order_amount):
            if self.order_quantity is None:
                raise ValueError("order_quantity is required when order_amount is not provided")
    
    def to_dict(self) -> dict:
        """Convert order to dictionary format for API requests"""
        data = {
            'symbol': self.symbol,
            'order_type': self.order_type,
            'side': self.side
        }
        
        # Add optional fields only if they differ from defaults
        if self.order_type != 'MARKET':
            data['order_price'] = self.order_price
            
        if not (self.order_type in ['MARKET', 'ASK', 'BID'] and self.order_amount):
            data['order_quantity'] = self.order_quantity
            
        if self.client_order_id != 12345:
            data['client_order_id'] = self.client_order_id
            
        if self.margin_mode != 'CROSS':
            data['margin_mode'] = self.margin_mode
            
        if self.order_tag != 'default':
            data['order_tag'] = self.order_tag
            
        if self.order_amount:
            data['order_amount'] = self.order_amount
            
        if self.reduce_only:
            data['reduce_only'] = self.reduce_only
            
        if self.visible_quantity is not None:
            data['visible_quantity'] = self.visible_quantity
            
        if self.position_side:
            data['position_side'] = self.position_side
        
        # add timestamp and latency
        data['timestamp'] = self.local_timestamp
        data['latency'] = self.estimated_latency
        
        return data