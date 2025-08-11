import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['RSI'] = compute_rsi(df['Close'])
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # fallback for early periods

def annualized_volatility(series: pd.Series, trading_days: int = 252) -> float:
    returns = series.pct_change().dropna()
    return returns.std() * np.sqrt(trading_days)

def compute_kpis(df: pd.DataFrame) -> dict:
    close = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
    kpis = {}
    kpis["latest_close"] = float(close.iloc[-1])
    kpis["1d_return_pct"] = float((close.iloc[-1] / close.iloc[-2] - 1) * 100) if len(close) >= 2 else 0.0
    kpis["30d_return_pct"] = float((close.iloc[-1] / close.iloc[-21] - 1) * 100) if len(close) >= 22 else 0.0
    kpis["sma_50"] = float(compute_sma(close, 50).iloc[-1])
    kpis["sma_200"] = float(compute_sma(close, 200).iloc[-1])
    kpis["rsi_14"] = float(compute_rsi(close, 14).iloc[-1])
    kpis["annual_volatility_pct"] = float(annualized_volatility(close) * 100)
    return kpis

def format_kpis_for_prompt(ticker: str, kpis: dict) -> str:
    lines = [
        f"Ticker: {ticker}",
        f"Latest Close: ${kpis['latest_close']:.2f}",
        f"1-day Return: {kpis['1d_return_pct']:.2f}%",
        f"30-day Return: {kpis['30d_return_pct']:.2f}%",
        f"SMA(50): ${kpis['sma_50']:.2f}",
        f"SMA(200): ${kpis['sma_200']:.2f}",
        f"RSI(14): {kpis['rsi_14']:.2f}",
        f"Annualized Volatility: {kpis['annual_volatility_pct']:.2f}%",
    ]
    return "\n".join(lines)