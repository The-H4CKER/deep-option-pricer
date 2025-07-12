# Deep Option Pricer

An advanced financial engineering project that leverages a deep neural network to price stock options by learning directly from real market data. This data-driven approach is designed to capture complex market dynamics, such as the **volatility smile**, which classic models like Black-Scholes cannot natively represent.

The project features an interactive web application built with Streamlit that serves as a tool for analysis and visualization, allowing for a direct comparison between the AI's learned pricing model and market reality.

## Key Features

* **AI-Powered Pricing Engine:** A neural network trained in PyTorch/TensorFlow predicts option prices based on historical data.
* **Volatility Smile Visualization:** An interactive Plotly chart that compares the market's true implied volatility smile against the smile learned by the AI model.
* **High-Performance Hybrid Core:** The core numerical loop is written in C++ and integrated with Python via `pybind11` to demonstrate performance optimization skills.
* **Automated Data Pipeline:** A data pipeline using `yfinance` and `SQLAlchemy` automatically ingests and stores daily option chain data in an SQLite database.
