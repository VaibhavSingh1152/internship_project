import requests
import pandas as pd

AMFI_URL = "https://www.amfiindia.com/spages/NAVAll.txt"


def load_nav_data():
    response = requests.get(AMFI_URL)
    lines = response.text.split("\n")

    data = []

    for line in lines:
        parts = line.split(";")

        if len(parts) > 5:
            try:
                scheme = parts[3].strip()
                nav = float(parts[4])
                date = parts[5].strip()

                data.append([scheme, nav, date])
            except:
                continue

    df = pd.DataFrame(data, columns=["scheme", "nav", "date"])

    # IMPORTANT FIX
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna()
    df = df.sort_values(["scheme", "date"])

    return df