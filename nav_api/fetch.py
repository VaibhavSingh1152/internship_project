import requests
import pandas as pd

def get_nav_history(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    data = requests.get(url).json()

    records = data["data"]

    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["nav"] = df["nav"].astype(float)

    df = df.sort_values("date")

    return df