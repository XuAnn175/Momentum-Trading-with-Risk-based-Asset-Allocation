## Alpha Signals

### 1. MACD (Moving Average Convergence Divergence)

* Definition: MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.

  $$
  \text{MACD} =EMA_{12} - EMA_{26}
  $$
* Components:

  * MACD Line: Difference between the 12-period and 26-period exponential moving averages (EMA).
  * Signal Line: 9-period EMA of the MACD line.
* Usage in Signal Generator:

  * Bullish Signal: When the MACD line crosses above the Signal line, indicating upward momentum.
  * Bearish Signal: When the MACD line crosses below the Signal line, indicating downward momentum.

### 2. OBV (On-Balance Volume)

$$
OBV_{t} =
  \begin{cases} 
  OBV_{t-1} + Volume_t & \text{if } Close_t > Close_{t-1} \\
  OBV_{t-1} - Volume_t & \text{if } Close_t < Close_{t-1} \\
  OBV_{t-1} & \text{if } Close_t = Close_{t-1}
  \end{cases}
$$

* Definition: OBV is a momentum indicator that uses volume flow to predict changes in stock price.
* Calculation: It cumulatively adds volume on up days and subtracts volume on down days.

  * Usage in SignalGenerator:
  * Slope of OBV (obv_slope): Measures the rate of change of OBV to assess the strength of the trend.
  * Positive Slope (> 0.5): Indicates strong upward momentum.
  * Negative Slope (< -0.5): Indicates strong downward momentum.

### 3. OBV Slope

The OBV Slope measures the average rate of change of the OBV over the past **n** periods. A positive slope indicates an upward trend in volume flow, while a negative slope suggests a downward trend.

Linear Regression Approach:

In the provided OBV class, the slope is calculated using linear regression over the window **n**. The slope **m** is determined by fitting a line to the OBV values in the current window:

$$
m = \frac{n\sum(xy) - \sum x \sum y}{n\sum(x^2) - (\sum x)^2}
$$

### **4. Rolling Maximum and Minimum**

Rolling Maximum and Rolling Minimum are statistical measures that represent the highest and lowest prices over a specified rolling window. They are used to identify key support and resistance levels.

**Mathematical Expression:**

$$
\text{rollin max}_t = max ( High(t-n+1),High(t-n+2),...High(t) )
$$

$$
\text{rollin min}_t = max ( Low(t-n+1),Low(t-n+2),...Low(t) )
$$

Where:

* **n** is the size of the rolling window.
* **High** and **Low** are the highest and lowest prices in the window, respectively.

## Signal Generation
