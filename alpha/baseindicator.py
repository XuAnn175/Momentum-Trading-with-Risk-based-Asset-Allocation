class BaseIndicator:
    def __init__(self):
        pass
    
    def calculate(self, df):
        raise NotImplementedError