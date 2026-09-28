from nav_api.search import search_fund
from nav_api.fetch import get_nav_history
from nav_module.ml_pipeline import prepare_features, train_model

import pandas as pd
import matplotlib.pyplot as plt


def main():

    # ===== INPUT =====
    query = input("Enter mutual fund name: ")

    print("\nSearching funds...\n")
    results = search_fund(query)

    if not results:
        print("No funds found")
        return

    for i, r in enumerate(results):
        print(f"{i}. {r['name']}")

    try:
        choice = int(input("\nSelect fund number: "))
    except:
        print("Invalid input")
        return

    if choice < 0 or choice >= len(results):
        print("Invalid selection")
        return

    selected = results[choice]

    print("\nSelected Fund:", selected["name"])

    # ===== FETCH DATA =====
    df = get_nav_history(selected["code"])
    print("Records loaded:", len(df))

    if len(df) < 30:
        print("Not enough historical data")
        return

    # ===== FEATURES =====
    df = prepare_features(df)

    if len(df) < 10:
        print("Not enough usable data")
        return

    # ===== MODEL =====
    model = train_model(df)

    latest = df.iloc[-1][["nav_prev", "rolling_mean", "rolling_std"]]
    latest_df = pd.DataFrame([latest])

    prediction = model.predict(latest_df)[0]

    current_nav = df["nav"].iloc[-1]

    # ===== SIGNAL ENGINE =====
    trend_score = (prediction - current_nav) / current_nav

    volatility = df["rolling_std"].iloc[-1] / df["rolling_mean"].iloc[-1]

    if trend_score > 0:
        signal = "BULLISH 🟢"
    else:
        signal = "BEARISH 🔴"

    confidence = abs(trend_score) * 100 + (1 - volatility) * 50
    confidence = max(0, min(100, confidence))

    # ===== OUTPUT =====
    print("\n===== NAV PREDICTION SYSTEM =====")
    print("Fund:", selected["name"])
    print("Predicted NAV:", round(prediction, 2))
    print("Current NAV:", round(current_nav, 2))

    print("\n===== MARKET SIGNAL =====")
    print("Signal:", signal)
    print("Confidence:", round(confidence, 2), "%")

    # ===== GRAPH =====
    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["nav"], label="NAV History")

    plt.scatter(df["date"].iloc[-1], prediction, color="red", label="Prediction")

    plt.title("NAV Trend + Prediction")
    plt.xlabel("Date")
    plt.ylabel("NAV")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()