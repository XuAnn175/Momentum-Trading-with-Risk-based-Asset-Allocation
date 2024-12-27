import numpy as np
from .baseindicator import BaseIndicator

class OBV(BaseIndicator):
    def __init__(self, slope_window=5):
        self.slope_window = slope_window
        
    def _calculate_slope(self, series):
        """Calculate slope using linear regression"""
        slopes = [np.nan] * len(series)
        for i in range(self.slope_window - 1, len(series)):
            y = series[i - self.slope_window + 1:i + 1]
            x = np.arange(self.slope_window)
            A = np.vstack([x, np.ones(len(x))]).T
            m, _ = np.linalg.lstsq(A, y, rcond=None)[0]
            slopes[i] = m
        return np.array(slopes)
        
    def calculate(self, df):
        """Calculate OBV and its slope"""
        df = df.copy()
        df['daily_ret'] = df['Adj Close'].pct_change()
        df['direction'] = np.where(df['daily_ret']>=0, 1, -1)
        df['direction'].iloc[0] = 0
        df['vol_adj'] = df['Volume'] * df['direction']
        df['obv'] = df['vol_adj'].cumsum()
        df['obv_slope'] = self._calculate_slope(df['obv'])
        return df[['obv', 'obv_slope']]
