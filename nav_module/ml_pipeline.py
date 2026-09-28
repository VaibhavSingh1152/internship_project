import pandas as pd
from sklearn.linear_model import LinearRegression

def prepare_features(df):
    df = df.copy()

    df["nav_prev"] = df["nav"].shift(1)
    df["rolling_mean"] = df["nav"].rolling(5).mean()
    df["rolling_std"] = df["nav"].rolling(5).std()

    df = df.dropna()

    return df


def train_model(df):
    X = df[["nav_prev", "rolling_mean", "rolling_std"]]
    y = df["nav"]

    model = LinearRegression()
    model.fit(X, y)

    return model