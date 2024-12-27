# GM(1,1) Grey Prediction Model

## 0. Our Flow of Thought

1. For the simuation of HFT, we don't want to use the state-of-the-art ML models for price prediction,which is also meaningless if we just copy the code and get super great accuracy but without our own thought.
2. Instead,we want to find some statistical models that can capture sophisticated pattern of price dynamics and predict the price using just a couple of caculations,which is important in HFT.
3. Our model for predicting price movements is not simply based on buying when prices rise and selling when prices fall. Instead, it is designed to calculate expected returns and risks, serving as a tool for asset allocation purposes.The trading signals are generated from our market microstructure analysis.

## 1. What is "Grey"?

In grey prediction, we need to understand three types of systems:

### White Systems

* Systems with completely known internal characteristics
* Given an input, we can accurately predict the output

### Black Systems

* Systems where internal information is unknown

### Grey Systems

- Systems between white and black systems
- Partial information is known, partial is unknown
- Relationships between factors are uncertain

## 2. Mathematical Foundation

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

## 3. $GM(1,1)$ Model Construction

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

## 4. Parameter Estimation

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

## 5. Prediction

Once $a$ and  $b$ are determined, the model can predict future values using the following formula:

$$
\hat{x}^{(1)}(k+1) = \left( x^{(0)}(1) - \frac{b}{a} \right) e^{-ak} + \frac{b}{a}
$$

To obtain the predicted values in the original data scale, the inverse AGO (IAGO) is applied:

$$
\hat{x}^{(0)}(k) = \hat{x}^{(1)}(k) - \hat{x}^{(1)}(k-1)
$$

## 6. Advantages and Limitations

### Advantages

- Suitable for small datasets with no obvious patterns
- Uses differential equations to uncover intrinsic patterns
- Effective for short-term prediction with fast speed

### Limitations

- Only suitable for short-term forecasting
- Best for quasi-exponential growth (類指數成長) patterns
- Requires passing the class ratio check

## 7. Application Steps

**Premise : Perform Quasi-Exponential Testing of Data**

1. Generate accumulated sequence (AGO)
2. Construct $GM(1,1)$ model
3. Estimate parameters using least squares
4. Generate predictions

Note: The model should be updated as new data becomes available.

# Experiment : The Quasi-Exponential Testing of Data

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
