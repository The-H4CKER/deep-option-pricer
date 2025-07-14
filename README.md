# Deep Option Pricer

An advanced financial engineering project that leverages a deep neural network to price stock options by learning directly from real market data. This data-driven approach is designed to capture complex market dynamics, such as the **volatility smile**, which classic models like Black-Scholes cannot natively represent.

The project features an interactive web application built with Streamlit that serves as a tool for analysis and visualization, allowing for a direct comparison between the AI's learned pricing model and market reality.

## Key Features

* **AI-Powered Pricing Engine:** A neural network trained in PyTorch predicts option prices based on historical data.
* **Volatility Smile Visualization:** An interactive Plotly chart that compares the market's true implied volatility smile against the smile learned by the AI model.
* **High-Performance Hybrid Core:** The core numerical loop is written in C++ and integrated with Python via `pybind11` to demonstrate performance optimization skills.
* **Automated Data Pipeline:** A data pipeline using `yfinance` and `SQLAlchemy` automatically ingests and stores daily option chain data in an SQLite database.

## Model Performance

The model was improved through a systematic, iterative process, resulting in two final models designed for different tasks.

### Model A: Maximum Predictive Accuracy

This model uses all available features, including **Implied Volatility**, to achieve the lowest possible prediction error.

* **Best Test RMSE: $4.97**
* **Conclusion:** By using the market's own volatility forecast (IV) as a feature, this model can predict option prices with high accuracy. This demonstrates the ability to build a powerful predictive tool.

### Model B: Fundamental Pricing (No Implied Volatility)

This model was intentionally given a harder task: predict the option price **without** seeing the implied volatility. This forces the model to learn the complex concept of volatility from scratch using only fundamental inputs (moneyness, time to expiry, etc.).

* **Best Test RMSE: $9.97**
* **Conclusion:** Achieving a single-digit RMSE without the most powerful predictive feature is a significant accomplishment. It proves the model's architecture is robust and capable of learning the deep, non-linear dynamics of option pricing from first principles.

#### Final Learning Curve (Model B)

The plot below shows the Test RMSE ($) vs. training epochs for the fundamental pricing model (Model B).

![Final Model Learning Curve](assets/final_learning_curve.png)
