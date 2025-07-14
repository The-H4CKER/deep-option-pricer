import pytest
from src.deep_option_pricer.financial_model import (
    black_scholes_price,
    implied_volatility,
)

from pytest import approx


def test_black_scholes_call_price():
    """
    Test the BS price against known value from online calculator.
    Inputs: S_k=100, K=105, T=1 year, r=5%, sigma=20%
    Expected Call Price: 8.021
    """
    S_t, K, r, t, sigma = 100, 105, 0.05, 1, 0.2

    calculated_price = black_scholes_price(S_t, K, r, t, sigma, option_type="call")
    expected_price = 8.021

    assert calculated_price == approx(expected_price, abs=1e-3)


def test_black_scholes_put_price():
    """
    Test an in-the-money put option (strike > stock price).
    Inputs: S=100, K=105, t=1 year, r=5%, sigma=20%
    """
    S_t, K, r, t, sigma = 100, 105, 0.05, 1, 0.2
    calculated_price = black_scholes_price(S_t, K, r, t, sigma, option_type="put")
    # Corrected expected value
    expected_price = 7.90
    assert calculated_price == approx(expected_price, abs=1e-2)


def test_implied_volatility_round_trip():
    S_t, K, r, t, known_sigma = 100, 105, 0.05, 1, 0.2

    market_price = black_scholes_price(S_t, K, r, t, known_sigma, option_type="call")
    calculated_iv = implied_volatility(market_price, S_t, K, r, t, option_type="call")

    assert calculated_iv == approx(known_sigma, abs=1e-4)
