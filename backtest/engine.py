from strategies import moving_average_crossover_strategy
from data import data_download

def backtest_engine(ticker, start_date, end_date):

    """Run the backtest engine for a given strategy and data."""

    signal = moving_average_crossover_strategy(ticker, start_date, end_date)
    return signal


def buy_shares(capital, price):
    """Calculate the number of shares to buy based on the signal."""
    return capital // price


def sell_shares(shares, price):
    """Calculate the number of shares to sell based on the signal."""
    return shares * price


def calculate_portfolio_value(shares, price):
    """Calculate the total portfolio value based on the number of shares and current price."""
    return shares * price


def trade(ticker, capital, start_date, end_date):
    """Execute trades based on the signal and update capital and shares."""

    signal = moving_average_crossover_strategy(ticker, start_date, end_date)
    price = data_download(ticker, start_date, end_date)
    new_df = price.to_frame()
    new_df['Signal'] = signal
    shares = 0
    try:

        if signal == 1:  # BUY
            shares = buy_shares(capital, price)
            capital -= shares * price
        elif signal == -1:  # SELL
            capital += sell_shares(shares, price)
            shares = 0
    except Exception as e:
        print(f"Error occurred while executing trade: {e}")

    return capital, shares

