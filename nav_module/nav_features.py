import pandas as pd

def create_features(df):
    df = df.copy()

    df["nav_prev"] = df["nav"].shift(1)
    df["return"] = df["nav"] - df["nav_prev"]

    df["rolling_mean"] = df["nav"].rolling(3).mean()
    df["rolling_std"] = df["nav"].rolling(3).std()

    df = df.dropna()

    return df