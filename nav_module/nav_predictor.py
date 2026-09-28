import yfinance as yf
import pandas as pd

def get_data(symbol="AAPL"):
    df = yf.download(symbol, period="6mo", interval="1d")
    df = df[["Close"]].dropna()
    df.columns = ["price"]
    return df

def add_features(df):
    df = df.copy()

    df["ma7"] = df["price"].rolling(7).mean()
    df["ma21"] = df["price"].rolling(21).mean()
    df["returns"] = df["price"].pct_change()

    df = df.dropna()
    return df

def predict_trend(df):
    last = df.iloc[-1]

    score = 0

    if last["ma7"] > last["ma21"]:
        score += 1
    else:
        score -= 1

    if last["returns"] > 0:
        score += 1
    else:
        score -= 1

    if score >= 1:
        return "Bullish"
    elif score <= -1:
        return "Bearish"
    else:
        return "Neutral"