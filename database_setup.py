import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

DB_NAME = "options_date.db"
DB_PATH = f"sqlite:///{DB_NAME}"

Base = declarative_base()


class OptionData(Base):
    __tablename__ = "options"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    fetch_timestamp = sa.Column(sa.DateTime, nullable=False)
    ticker = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    option_type = sa.Column(sa.String, nullable=False)  # 'call' or 'put'
    expiry_date = sa.Column(sa.Date, nullable=False)
    strike_price = sa.Column(sa.Float, nullable=False)
    market_price = sa.Column(sa.Float, nullable=False)
    implied_volatility = sa.Column(sa.Float, nullable=False)
    time_to_expiry_days = sa.Column(sa.Integer, nullable=False)


def create_database():
    print("Setting up database...")
    engine = sa.create_engine(DB_PATH)

    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == "__main__":
    create_database()
