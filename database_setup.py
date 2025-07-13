import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

DB_NAME = "options_date.db"
DB_PATH = f"sqlite:///{DB_NAME}"

Base = declarative_base()


class OptionData(Base):
    """
    ORM model 'options' table.
    Represents a single options contract.

    Attributes:
        id (int): Unique identifier for the option.
        fetch_timestamp (datetime): Timestamp when the data was fetched.
        ticker (str): Stock ticker symbol.
        stock_price (float): Price of the underlying stock.
        option_type (str): Type of option ('call' or 'put').
        expiry_date (date): Expiration date of the option.
        strike_price (float): Strike price of the option.
        market_price (float): Market price of the option.
        implied_volatility (float): Implied volatility of the option.
        dte (int): Days until the option expires.
    """

    __tablename__ = "options"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    fetch_timestamp = sa.Column(sa.DateTime, nullable=False)
    ticker = sa.Column(sa.String, nullable=False)
    stock_price = sa.Column(sa.Float, nullable=False)
    option_type = sa.Column(sa.String, nullable=False)
    expiry_date = sa.Column(sa.Date, nullable=False)
    strike_price = sa.Column(sa.Float, nullable=False)
    market_price = sa.Column(sa.Float, nullable=False)
    implied_volatility = sa.Column(sa.Float, nullable=False)
    dte = sa.Column(sa.Integer, nullable=False)

    def __repr__(self):
        return (
            f"<OptionData(ticker='{self.ticker}', "
            f"type='{self.option_type}', "
            f"strike={self.strike_price}, "
            f"expiry='{self.expiry_date}')>"
        )


def create_database():
    print("Setting up database...")
    engine = sa.create_engine(DB_PATH)

    try:
        print("Creating table if it does not exist...")
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    create_database()
