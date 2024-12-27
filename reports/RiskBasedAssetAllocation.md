# Risk Based Asset Allocation Method

In the context of trading strategies,, it's crucial to balance the objectives of**maximizing profit** and **minimizing risk**. The **Objective Planning Equation** we designed serves as a mathematical framework to achieve this balance. Below is the detailed  explanation.

## 1. Maximizing Profit

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

## 2. Minimizing Risk

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

## 3. Combining Profit and Risk: The Multi-Objective Planning Equation

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

## 4. Constraints

To ensure the feasibility and practicality of the optimization, several constraints are imposed:

### **Budget Constraint:**

$$
\sum_{j=1}^{n} p_t^{(j)} x_j \leq \text{Total Capital}
$$

Ensures that the total capital is not exceeded.

### **Non-Negativity:**

Ensuring that holdings are non-negative.

$$
h_j \geq 0 \quad \forall j
$$

### **Commission Constraints:**

$$
\sum_{j=1}^{n} p_t^{(j)} x_j \alpha_j \leq \sum_{j=1}^{n} abs(p_t^{(j)} - \hat{p}_{t+1}^{(j)}) x_j
$$

Where:

- $x_j$ = Transaction volume for asset $j$
- $\alpha_j$ = Transaction commission ratio for asset $j$

This ensures that commission should not be greater than the profit.

## 5. Combination of Objective function & Constraints

Based on the aforementioned objective function and constraints, the optimal trading volume can be determined for different numbers of investment portfolios (n).

* When **n=1,** the objective function is a 2-D line. After applying the constraints, it forms a line segment. The optimal trading volume is found at the maximum point on this segment.
  ![img](https://imgur.com/XyQ3kTE.png)
* When **n=2**, the objective function becomes a plane. The optimal trading volume combination $(x_1, x_2)$ is found at the maximum point within this plane.
  ![img](https://imgur.com/WXi9SUb.png)
