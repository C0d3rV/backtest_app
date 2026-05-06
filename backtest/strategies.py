from data import data_download
import pandas as pd


def moving_average_crossover_strategy(ticker, start_date, end_date):

    """Implement a simple moving average crossover strategy."""
    try:
        close_prices_series = data_download(ticker, start_date, end_date)
    except ValueError as e:
        print(f"Error getting data from data_download: {e}")
        return

    short_ma = close_prices_series.rolling(window=50).mean()
    long_ma = close_prices_series.rolling(window=200).mean()
    signal = pd.Series(index=close_prices_series.index, dtype = float)
    signal[short_ma > long_ma] = 1  #BUY
    signal[short_ma == long_ma] = 0 #HOLD
    signal[short_ma < long_ma] = -1  #SELL

    return signal