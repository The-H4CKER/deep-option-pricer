import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq


def black_scholes_price(S_t, K, r, t, sigma, option_type="call"):
    """
    Calculates Black-Scholes option price.

    Args:
        S_t: spot price of an asset
        K: strike price
        r: risk-free interest rate
        t: time to maturity
        sigma: volatility of the asset

    Returns:
        C: call option price
    """
    # N(d1) = probability the option is exercised
    # N(d2) = probability that the option finishes in the money
    d1 = (np.log(S_t / K) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)

    if option_type == "call":
        C = S_t * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    elif option_type == "put":
        C = K * np.exp(-r * t) * norm.cdf(-d2) - S_t * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    return C


def implied_volatility(C, S_t, K, r, t, option_type="call"):
    """Reverse-engineer volatility from option price using brentq solver"""

    def price_error(sigma):
        return black_scholes_price(S_t, K, r, t, sigma, option_type) - C

    try:
        # Search for a volatility between 0.1% and 1000%
        sigma = brentq(price_error, a=0.001, b=10.0, maxiter=100)
    except ValueError:
        sigma = np.nan

    return sigma
