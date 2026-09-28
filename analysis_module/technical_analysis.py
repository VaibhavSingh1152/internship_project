import yfinance as yf
import pandas as pd


def get_stock_data(symbol, period="6mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)
    return df


def calculate_indicators(df):
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    return df


def generate_trend_signal(df):
    df = df.dropna()

    if len(df) < 50:
        return "INSUFFICIENT_DATA"

    last = df.iloc[-1]

    sma20 = last["SMA_20"]
    sma50 = last["SMA_50"]
    price = last["Close"]

    if hasattr(sma20, "iloc"):
        sma20 = sma20.iloc[0]
    if hasattr(sma50, "iloc"):
        sma50 = sma50.iloc[0]
    if hasattr(price, "iloc"):
        price = price.iloc[0]

    if price > sma20 and sma20 > sma50:
        return "BULLISH"
    elif price < sma20 and sma50 < sma20:
        return "BEARISH"
    else:
        return "NEUTRAL"