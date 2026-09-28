from sklearn.linear_model import LinearRegression
import numpy as np


def train_model(df):
    X = df[["nav_prev", "rolling_mean", "rolling_std"]]
    y = df["nav"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_next(model, latest_row):
    X = np.array(latest_row).reshape(1, -1)
    return model.predict(X)[0]