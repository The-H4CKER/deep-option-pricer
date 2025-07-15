import streamlit as st
import torch
import numpy as np
import joblib
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go

from src.deep_option_pricer.model import OptionPricer
from src.deep_option_pricer.financial_model import implied_volatility

# --- Page Configuration ---
st.set_page_config(page_title="Deep Option Pricer", page_icon="📊", layout="wide")


# --- Model and Scaler Loading ---
@st.cache_resource
def load_assets():
    """Load the trained model and scaler."""
    input_size = 6
    model = OptionPricer(input_size)
    model.load_state_dict(torch.load("models/best_model.pth"))
    model.eval()
    scaler = joblib.load("models/scaler.joblib")
    return model, scaler


model, scaler = load_assets()


# --- Functions ---
@st.cache_data
def get_stock_data(ticker_symbol):
    """Fetches stock data and expiration dates."""
    ticker = yf.Ticker(ticker_symbol)
    expirations = ticker.options
    stock_price = round(ticker.history(period="1d")["Close"].iloc[-1], 2)
    return stock_price, expirations


# --- Page UI ---
st.title("Deep Option Pricer")
st.write(
    "An AI-powered option pricing model that learns the volatility smile from fundamental data."
)

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("Volatility Smile Visualizer")
    ticker_symbol = st.text_input("Stock Ticker", value="AAPL").upper()

    try:
        stock_price, expirations = get_stock_data(ticker_symbol)
        st.success(f"Current {ticker_symbol} Price: ${stock_price}")
        expiry_selection = st.selectbox("Select Expiration Date", expirations)
        visualize_button = st.button("Visualize Smile", use_container_width=True)
    except Exception as e:
        st.error(f"Could not fetch data for {ticker_symbol}. Please check the ticker.")
        visualize_button = False

# --- Main Content Area ---
if visualize_button:
    with st.spinner("Fetching data and generating AI predictions..."):
        # Fetch live option chain data
        option_chain = yf.Ticker(ticker_symbol).option_chain(expiry_selection)
        calls = option_chain.calls.dropna(
            subset=["strike", "lastPrice", "impliedVolatility"]
        )

        # Prepare features for the entire chain
        dte = (datetime.strptime(expiry_selection, "%Y-%m-%d") - datetime.now()).days
        r_decimal = 0.05  # Placeholder risk-free rate

        features_list = []
        for i, row in calls.iterrows():
            moneyness = stock_price / row["strike"]
            features = [
                stock_price,
                row["strike"],
                dte,
                r_decimal,
                0.0,  # call
                moneyness,
            ]
            features_list.append(features)

        features_array = np.array(features_list)
        features_scaled = scaler.transform(features_array)
        features_tensor = torch.tensor(features_scaled, dtype=torch.float32)

        # Get AI price predictions
        with torch.no_grad():
            ai_log_prices = model(features_tensor)
        ai_prices = torch.exp(ai_log_prices).numpy().flatten()
        calls["ai_price"] = ai_prices

        # Calculate AI Learned Implied Volatility
        ai_ivs = []
        for i, row in calls.iterrows():
            iv = implied_volatility(
                row["ai_price"],
                stock_price,
                row["strike"],
                dte / 365,
                r_decimal,
                "call",
            )
            ai_ivs.append(iv)
        calls["ai_iv"] = ai_ivs

        # Plot the smiles
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=calls["strike"],
                y=calls["impliedVolatility"],
                mode="lines+markers",
                name="Market Smile",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=calls["strike"],
                y=calls["ai_iv"],
                mode="lines+markers",
                name="AI Learned Smile",
            )
        )

        fig.update_layout(
            title=f"Volatility Smile Comparison for {ticker_symbol} (Expires: {expiry_selection})",
            xaxis_title="Strike Price ($)",
            yaxis_title="Implied Volatility",
            legend_title="Smile Source",
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info(
        "Select a ticker and expiration date in the sidebar to visualize the volatility smile."
    )
