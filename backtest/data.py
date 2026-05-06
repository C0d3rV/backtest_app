import yfinance as yf
import pandas as pd
import datetime


def data_download(ticker, start_date, end_date):

    """Download historical stock data for Tciker from Yahoo Finance. Return a pandas Series of closing prices."""

    if not isinstance(ticker, str):
        raise ValueError("Ticker symbol must be a string.")
    
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        raise ValueError("Start date and end date must be strings in the format 'YYYY-MM-DD'.")

    if not ticker:
        raise ValueError("Ticker symbol is required.")
    
    if not start_date or not end_date:
        raise ValueError("Start date and end date are required.")
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    if start_date >= end_date:
        raise ValueError("Start date must be earlier than end date.")

    try:
        df = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        raise ValueError(f"Error downloading data for ticker {ticker}: {e}")

    if df.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
    try:
        close_prices_series = df['Close'][ticker]
    except KeyError:
        raise ValueError(f"Close price data not found for ticker: {ticker}")
    
    return close_prices_series 