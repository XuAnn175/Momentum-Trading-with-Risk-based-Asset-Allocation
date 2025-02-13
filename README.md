# 1. Strategy Overview

![img](https://imgur.com/8PBicC0.png)

1. Price Prediction using Grey Model: The GM(1,1) model generates future price predictions for Bitcoin (Chap. 3)
2. Market Momemtum Analysis for Trading Signals Generation: Our finanacial market momemtum analysis would generate buy/sell singals.(Chap. 4)
3. Risk Based Asset Allocation: Our designed objective function optimizes the allocation of assets based on predicted returns and associated risks. (Chap. 5)

# 2. Results

## 2.1 : Return of Our Strategy v.s. Return of holding BTC in a 5-Day Period

Point of Buy and Sell is also plotted in the graph.

![img](https://imgur.com/ujuNs4k.png)

## 2.2 : Signal Generation

![img](https://imgur.com/TnXJWoH.png)

## 3.GM(1,1) Grey Prediction Model

## 3.0 : Our Flow of Thought

1. For the simuation of HFT, we don't want to use the state-of-the-art ML models for price prediction,which is also meaningless if we just copy the code and get super great accuracy but without our own thought.
2. Instead,we want to find some statistical models that can capture sophisticated pattern of price dynamics and predict the price using just a couple of caculations,which is important in HFT.
3. Our model for predicting price movements is not simply based on buying when prices rise and selling when prices fall. Instead, it is designed to calculate expected returns and risks, serving as a tool for asset allocation purposes.

## 3.1 :  What is "Grey"?

In grey prediction, we need to understand three types of systems:

#### White Systems

* Systems with completely known internal characteristics
* Given an input, we can accurately predict the output

#### Black Systems

* Systems where internal information is unknown

#### Grey Systems

- Systems between white and black systems
- Partial information is known, partial is unknown
- Relationships between factors are uncertain

## 3.2. Mathematical Foundation

### Original Sequence

Let the original sequence (prices) be:

$$
X^{(0)} = \{ x^{(0)}(1), x^{(0)}(2), \ldots, x^{(0)}(n) \}
$$

### Accumulated Generating Operation (AGO)

To reduce randomness in the data and highlight the trend, the AGO is applied,

The accumulated sequence $x^{(1)}$ is generated as:

$$
x^{(1)}(k) = \sum_{i=1}^{k} x^{(0)}(i), \quad k = 1, 2, \ldots, n
$$

## 3.3 : $GM(1,1)$ Model Construction

The newly generated sequence and the visual trend  appear to form an exponential curve (or a straight line) in a short period. In such cases, an exponential curve or even a straight-line expression can be used to approximate this trend.

Once this expression is obtained, the problem is effectively solved.

But how can we determine the "expression for an exponential curve or a straight line"?

From calculus knowledge, we know that the general solution to a first-order ordinary differential equation is an exponential function. Therefore, by constructing a first-order ordinary differential equation and solving it, we can derive the desired function expression.

The $GM(1,1)$ model is based on a first-order differential equation:

$$
\frac{d x^{(1)}}{dt} + a x^{(1)}(t) = b
$$

where:

- a is the development coefficient
- b is the grey input

## 3.4 : Parameter Estimation

##### Discrete Form

Since data is discrete $(dt = 1)$, the differential equation is approximated in discrete form:

$$
x^{(0)}(k) + a z^{(1)}(k) = b
$$

where $z{(1)}(k)$ is the adjacent mean sequence defined as:

$$
z^{(1)}(k) = \frac{1}{2} [x^{(1)}(k) + x^{(1)}(k-1)], \quad k = 2, 3, \ldots, n
$$

To estimate the parameters $a$ and $b$, the method of least squares is employed. This involves setting up the following equations based on the discrete model:

$$
\begin{cases}
  x^{(0)}(2) + a z^{(1)}(2) = b \\
  x^{(0)}(3) + a z^{(1)}(3) = b \\
  \vdots \\
  x^{(0)}(n) + a z^{(1)}(n) = b
\end{cases}
$$

This can be rewritten in matrix form as:

$$
Y = B\Theta
$$

where:

$$
Y = [x^{(0)}(2), x^{(0)}(3), \ldots, x^{(0)}(n)]^T
$$

$$
B = \begin{bmatrix}
-z^{(1)}(2) & 1 \\
-z^{(1)}(3) & 1 \\
\vdots & \vdots \\
-z^{(1)}(n) & 1
\end{bmatrix}
$$

$$
\Theta = \begin{bmatrix} a \\ b \end{bmatrix}
$$

Using the least squares method, the parameter vector $\Theta$ is estimated as:

$$
\Theta = (B^T B)^{-1} B^T Y
$$

## 3.5 : Prediction

Once $a$ and  $b$ are determined, the model can predict future values using the following formula:

$$
\hat{x}^{(1)}(k+1) = \left( x^{(0)}(1) - \frac{b}{a} \right) e^{-ak} + \frac{b}{a}
$$

To obtain the predicted values in the original data scale, the inverse AGO (IAGO) is applied:

$$
\hat{x}^{(0)}(k) = \hat{x}^{(1)}(k) - \hat{x}^{(1)}(k-1)
$$

## 3.6 : Advantages and Limitations

### Advantages

- Suitable for small datasets with no obvious patterns
- Uses differential equations to uncover intrinsic patterns
- Effective for short-term prediction with fast speed

### Limitations

- Only suitable for short-term forecasting
- Best for quasi-exponential growth (類指數成長) patterns
- Requires passing the class ratio check

## 3.7: Application Steps

**Premise : Perform Quasi-Exponential Testing of Data**

1. Generate accumulated sequence (AGO)
2. Construct $GM(1,1)$ model
3. Estimate parameters using least squares
4. Generate predictions

Note: The model should be updated as new data becomes available.

## 3.8 : Experiment : The Quasi-Exponential Testing of Data

The quasi-exponential test is a prerequisite check to determine whether a data series is suitable for GM(1,1) modeling. It verifies if the data follows an exponential-like growth or decay pattern.

The smoothness ratio of the initial sequence $X(0)$ is defined as:

$$
\rho(k) = \frac{x^{(0)}(k)}{x^{(1)}(k-1)}
$$

Where:

* $x^{(0)}(k)$ is the original data at period k
* $x^{(1)}(k - 1)$ is the accumulated (AGO) value at period k-1

In practical computations, it suffices to ascertain that over **80%** of the data points possess a smoothing ratio of less than **0.5** to conclude that the cumulative data adheres to the quasi-exponential law and can be used with the GM(1,1) model.

**Experimental Result :**

![img](https://imgur.com/G7zoBqa.png)

* The experimental result demonstrates that starting from the third period of data, Bitcoin data sequence exhibits a smoothing ratio consistently below 0.5. moreover, the proportion of periods with a smoothing ratio below 0.5 exceeds 80%. Consequently, the data sequence has
  successfully *passed* the quasi-exponential test, thereby ensuring their suitability for modeling
  using the grey prediction model.

# 4. Alpha Signals

## 4.1. MACD (Moving Average Convergence Divergence)

* Definition: MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.

  $$
  MACD=EMA_{12} - EMA_{26}
  $$
* Components:

  * MACD Line: Difference between the 12-period and 26-period exponential moving averages (EMA).
  * Signal Line: 9-period EMA of the MACD line.
* Usage in Signal Generator:

  * Bullish Signal: When the MACD line crosses above the Signal line, indicating upward momentum.
  * Bearish Signal: When the MACD line crosses below the Signal line, indicating downward momentum.

## 4.2. OBV (On-Balance Volume)

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

## 4.3. OBV Slope

The OBV Slope measures the average rate of change of the OBV over the past **n** periods. A positive slope indicates an upward trend in volume flow, while a negative slope suggests a downward trend.

Linear Regression Approach:

In the provided OBV class, the slope is calculated using linear regression over the window **n**. The slope **m** is determined by fitting a line to the OBV values in the current window:

$$
m = \frac{n\sum(xy) - \sum x \sum y}{n\sum(x^2) - (\sum x)^2}
$$

## **4.4. Rolling Maximum and Minimum**

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


# 5.Risk Based Asset Allocation Method

In the context of trading strategies,, it's crucial to balance the objectives of**maximizing profit** and **minimizing risk**. The **Objective Planning Equation** we designed serves as a mathematical framework to achieve this balance. Below is the detailed  explanation.

## 5.1: Maximizing Profit

### **Objective:**

The primary goal for any trading strategy is to **maximize returns** on investments. This involves allocating assets in a manner that leverages predicted price movements to generate the highest possible profit.

#### **Mathematical Representation:**

Let:

- $x_j$ = Transaction volume of asset $j$
- $p_t$ = Current price of asset $j$
- $\hat{p}_{t+1}$= Predicted price of asset \( j \) for the next period

The expected profit from asset \( j \) can be represented as:

$$
\text{Profit} =  \frac{abs(\hat{p}_{t+1} - p_t)} {p_t}  * x_j
$$

### **Total Expected Profit:**

$$
max \text{ Total Profit} = \sum_{j=1}^{n} ( \frac {abs(\hat{p}_{t+1}^{(j)} - p_t^{(j)})} {p_t} ) * x_j
$$

where \( n \) is the number of assets.

## 5.2 : Minimizing Risk

### **Objective:**

While maximizing profit is essential, it's equally important to **minimize risk** to ensure the sustainability of the trading strategy. Risk involves the potential for losses due to unfavorable market volatility.

### **Mathematical Representation:**

Let:

- $\rho_j$  = Risk factor (standard deviation of fixed size window) for asset $j$
- $x_j$ = Transaction volume of asset $j$

The risk associated with asset \( j \) can be represented as:

$$
\text{Risk}_j = \rho_j x_j
$$

$$
where \text{ } \rho_j = std(sliding \text{ } window)
$$

### **Total Risk:**

$$
\text{Total Risk} = min \sum_{j=1}^{n} \rho_j x_j
$$

$$
= max \sum_{j=1}^{n} -\rho_j x_j
$$

## 5.3 : Combining Profit and Risk: The Multi-Objective Planning Equation

### **Objective Function:**

To create a balanced trading strategy, we need to **maximize profit** while **minimizing risk** simultaneously. This is achieved by formulating a **multi-objective optimization problem** where both objectives are incorporated into a single objective function using a weighting coefficient.

### **Weighting Coefficient $\mu$ :**

- $\mu$ = Weight assigned to the profit objective.
- $1 - \mu$= Weight assigned to the risk objective.
- Typically, $0 \leq \mu \leq 1$ allowing flexibility in prioritizing profit over risk or vice versa based on investor preferences.
- **High $\mu$ (e.g., 0.7):** Prioritizes profit over risk, suitable for aggressive investors.
- **Low  $\mu$  (e.g., 0.3):** Prioritizes risk minimization, suitable for conservative investors.
- **Balanced $\mu$ (e.g., 0.5):** Maintains an balance between profit and risk.

### **Combined Objective Function:**

$$
max \text{ Objective} = \mu * \text {Total Profit}  + (1 - \mu) * \text{Total Risk}
$$

$$
\text{ = } \mu \left[  \sum ( \frac { |\hat{p}_{t+1}^{(j)} - p_t^{(j)}|} {p_t} ) * x_j \right] + (1 - \mu) \left[ - \sum \rho_j x_j \right]
$$

### **Explanation:**

- **Profit Component ( $\mu$ term):** Encourages the holding of assets to increase the portfolio's value.
- **Risk Component ( $1 - \mu$ term):** Penalizes high-risk holdings to discourage excessive exposure to volatile assets.

### **Optimization Goal:**

$$
\text{Maximize: } \text{Objective}
$$

By optimizing this objective function, the model seeks to find the optimal allocation \($h_j$) for each asset that provides the highest possible profit while keeping the associated risk within acceptable limits.

## 5.4 : Constraints

To ensure the feasibility and practicality of the optimization, several constraints are imposed:

### **Budget Constraint:**

$$
\sum_{j=1}^{n} p_t^{(j)} x_j \leq \text{Total Capital}
$$

Ensures that the total capital is not exceeded.

### **Non-Negativity:**

Ensuring that trading amount are non-negative.

$$
x_j \geq 0 \quad \forall j
$$

### **Commission Constraints:**

$$
\sum_{j=1}^{n} p_t^{(j)} x_j \alpha_j \leq \sum_{j=1}^{n} abs(p_t^{(j)} - \hat{p}_{t+1}^{(j)}) x_j
$$

Where:

- $x_j$ = Transaction volume for asset $j$
- $\alpha_j$ = Transaction commission ratio for asset $j$

This ensures that commission should not be greater than the profit.

## 5.5 : Combination of Objective function & Constraints

Based on the aforementioned objective function and constraints, the optimal trading volume can be determined for different numbers of investment portfolios (n).

* When **n=1,** the objective function is a 2-D line. After applying the constraints, it forms a line segment. The optimal trading volume is found at the maximum point on this segment.
  ![img](https://imgur.com/XyQ3kTE.png)
* When **n=2**, the objective function becomes a plane. The optimal trading volume combination $(x_1, x_2)$ is found at the maximum point within this plane.
  ![img](https://imgur.com/WXi9SUb.png)
