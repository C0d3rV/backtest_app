from strategies import moving_average_crossover_strategy

def backtest_engine(capital_amount, ticker, start_date, end_date):

    """
    Run the backtest engine for a given strategy and data.
    """

    signal = moving_average_crossover_strategy(ticker, start_date, end_date)
    return signal

backtest_result = backtest_engine(10000, 'AAPL', '2020-01-01', '2021-01-01')
print(backtest_result.tail())