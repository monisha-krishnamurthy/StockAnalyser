import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    df = yf.download(ticker, period=period, progress=False)
    if df.empty:
        raise ValueError(f"No data for ticker {ticker}")
    return df 