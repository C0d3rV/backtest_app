from strategies import moving_average_crossover_strategy
from data import data_download
import pandas as pd

def backtest_engine(capital, ticker, start_date, end_date):

    """Run the backtest engine for a given strategy and data."""

    try:
        closed_price_series = data_download(ticker, start_date, end_date)
    except Exception as e:
        print(f"Error occurred while downloading data: {e}")
        return
    try:
        signal = moving_average_crossover_strategy(ticker, start_date, end_date)
    except Exception as e:
        print(f"Error occurred while generating signal: {e}")
        return
    
    new_df = pd.DataFrame({'Close': closed_price_series, 'Signal': signal})

    new_df['capital'] = float(capital)
    new_df['shares'] = 0

    new_df = new_df.dropna(subset=['Signal'])
    new_df = new_df.reset_index(drop=True)

    try:
        for i in range(1, len(new_df)):
            previous_capital = new_df.loc[i-1, 'capital']
            previous_shares = new_df.loc[i-1, 'shares']

            current_signal = new_df.loc[i, 'Signal']
            current_price = new_df.loc[i, 'Close']

            if current_signal == 1 and previous_capital >= current_price:
                shares_to_buy = previous_capital // current_price
                new_df.loc[i, 'shares'] = shares_to_buy
                new_df.loc[i, 'capital'] = previous_capital - (shares_to_buy * current_price)

            elif current_signal == -1 and previous_shares > 0:
                new_df.loc[i, 'capital'] = previous_capital + (previous_shares * current_price)
                new_df.loc[i, 'shares'] = 0

            else:
                new_df.loc[i, 'capital'] = previous_capital
                new_df.loc[i, 'shares'] = previous_shares
    except Exception as e:
        print(f"Error occurred during backtest simulation: {e}")
        return
    
    #final_row = new_df.iloc[-1]
    #profit_loss = final_row['capital'] + (final_row['shares'] * final_row['Close']) - capital
    return new_df



def trade_stats(capital, ticker, start_date, end_date):
    """Calculate trade statistics from the backtest result."""

    trade_data = backtest_engine(capital, ticker, start_date, end_date)
    initial_capital = capital

    total_gains  = (trade_data['capital'].iloc[-1] - initial_capital) / initial_capital * 100

    total_buy = len(trade_data[trade_data['Signal'] == 1])
    total_sell = len(trade_data[trade_data['Signal'] == -1])
    total_trades = total_buy + total_sell

    for i in range(1, len(trade_data)):
        current_row = trade_data.iloc[i]
        previous_row = trade_data.iloc[i-1]

        trade_data['daily_pnl'] = (current_row['capital'] - previous_row['capital']) / previous_row['capital'] * 100

    return total_gains, total_trades, trade_data


gains, trades, trade_sheet = trade_stats(
    capital=100000, 
    ticker='YESBANK.NS', 
    start_date='2024-01-01', 
    end_date='2026-05-01'
    )


print(f"Total Profit/Loss: {gains:.2f}%")

trade_sheet.to_csv('yes_backtest_results.csv', index=True)