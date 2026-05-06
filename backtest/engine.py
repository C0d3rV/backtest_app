from strategies import moving_average_crossover_strategy

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


def trade(signal, capital, price):
    """Execute trades based on the signal and update capital and shares."""

    if not isinstance(signal, (int, float)):
        raise ValueError("Signal must be a numeric value.")
    
    if not isinstance(capital, (int, float)):
        raise ValueError("Capital must be a numeric value.")
    
    if not isinstance(price, (int, float)):
        raise ValueError("Price must be a numeric value.")
    
    if not signal:
        raise ValueError("Signal is missing.")
    
    if capital is None:
        raise ValueError("Capital is missing.") 
    
    if price is None:
        raise ValueError("Price is missing.")

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
