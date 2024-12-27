from .baseindicator import BaseIndicator

class ResistanceLines(BaseIndicator):
    def __init__(self, window=20):
        self.window = window
        
    def calculate(self, df):
        """Calculate rolling max/min resistance lines"""
        df = df.copy()
        df['rollin_max'] = df['High'].rolling(self.window).max()
        df['rollin_min'] = df['Low'].rolling(self.window).min()
        return df[['rollin_max', 'rollin_min']]
