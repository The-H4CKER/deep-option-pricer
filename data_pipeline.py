from datetime import datetime

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from typing import cast, Iterable, Dict, Any

from database_setup import OptionData, DB_PATH


def get_session():
    """Initialize and return a new database session."""
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    return Session()


def process_data(
    raw_df, option_type, expiry_date_ts, fetch_time, ticker_symbol, stock_price
):
    required_columns = ["strike", "lastPrice", "impliedVolatility"]
    clean_df = raw_df.dropna(subset=required_columns)
    df = clean_df[required_columns].copy()

    df.rename(
        columns={
            "strike": "strike_price",
            "lastPrice": "market_price",
            "impliedVolatility": "implied_volatility",
        },
        inplace=True,
    )

    df["fetch_timestamp"] = fetch_time
    df["ticker"] = ticker_symbol
    df["stock_price"] = stock_price
    df["option_type"] = option_type
    df["expiry_date"] = pd.to_datetime(expiry_date_ts)
    df["dte"] = (df["expiry_date"] - pd.to_datetime(fetch_time)).dt.days
    return df


def main():
    TICKER_SYMBOL = "AAPL"
    print(f"--- Starting data pipeline for {TICKER_SYMBOL} ---")

    session = get_session()
    ticker = yf.Ticker(TICKER_SYMBOL)

    stock_info = ticker.history(period="1d")
    if stock_info.empty:
        print(f"No stock data found for {TICKER_SYMBOL}.")
        return

    current_stock_price = round(stock_info["Close"].iloc[-1], 2)
    fetch_timestamp = datetime.now()

    total_records_added = 0
    expiration_dates = ticker.options

    for expiry in expiration_dates:
        option_chain = ticker.option_chain(expiry)

        calls_df = process_data(
            option_chain.calls,
            "call",
            expiry,
            fetch_timestamp,
            TICKER_SYMBOL,
            current_stock_price,
        )

        puts_df = process_data(
            option_chain.puts,
            "put",
            expiry,
            fetch_timestamp,
            TICKER_SYMBOL,
            current_stock_price,
        )

        combined_df = pd.concat([calls_df, puts_df])
        # type-checker complains on bulk-insert without casting key to string
        records = cast(Iterable[Dict[str, Any]], combined_df.to_dict(orient="records"))
        if not records:
            continue

        session.bulk_insert_mappings(inspect(OptionData), records)
        total_records_added += len(combined_df)

    try:
        session.commit()
        print(f"\n--- Pipeline finished ---")
        print(
            f"Successfully added {total_records_added} option records to the database."
        )
    except Exception as e:
        print(f"Failed to commit to database. Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()
