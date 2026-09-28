import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nav_api.search import search_fund
from nav_api.fetch import get_nav_history
from nav_module.ml_pipeline import prepare_features, train_model

from news_module.fetch_news import get_news
from news_module.sentiment import analyze_headlines
#from news_module.explanation import generate_explanation



# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI NAV Predictor",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Mutual Fund NAV Prediction Dashboard")


# ================= SIDEBAR =================

st.sidebar.header("🔍 Fund Search")

query = st.sidebar.text_input(
    "Enter Mutual Fund Keyword"
)

if not query:
    st.info(
        "Enter a mutual fund keyword in the sidebar to start analysis."
    )
    st.stop()


# ================= SEARCH FUND =================

results = search_fund(query)

if not results:
    st.error("No funds found")
    st.stop()

fund_names = [r["name"] for r in results]

selected_name = st.sidebar.selectbox(
    "Select Fund",
    fund_names
)

selected = next(
    r for r in results
    if r["name"] == selected_name
)

st.success(f"Selected Fund: {selected_name}")


# ================= LOAD NAV DATA =================

df = get_nav_history(selected["code"])

st.write(f"📊 Total Records: {len(df)}")

if len(df) < 10:
    st.error(
        "Too little historical data available for prediction."
    )
    st.stop()

elif len(df) < 30:
    st.warning(
        f"Only {len(df)} records available. Prediction confidence may be low."
    )


# ================= ML PIPELINE =================

df = prepare_features(df)

model = train_model(df)

latest = df.iloc[-1][
    ["nav_prev", "rolling_mean", "rolling_std"]
]

latest_df = pd.DataFrame([latest])

prediction = model.predict(latest_df)[0]

current_nav = df["nav"].iloc[-1]


# ================= SIGNAL ENGINE =================

trend_score = (
    prediction - current_nav
) / current_nav

volatility = (
    df["rolling_std"].iloc[-1]
    /
    df["rolling_mean"].iloc[-1]
)

signal = (
    "BULLISH 🟢"
    if trend_score > 0
    else "BEARISH 🔴"
)

confidence = (
    abs(trend_score) * 100
    +
    (1 - volatility) * 50
)

confidence = max(
    0,
    min(100, confidence)
)


# ================= PREDICTION OVERVIEW =================

st.subheader("📈 Prediction Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current NAV",
    round(current_nav, 2)
)

col2.metric(
    "Predicted NAV",
    round(prediction, 2)
)

col3.metric(
    "Records",
    len(df)
)


# ================= SIGNAL =================

st.subheader("📊 Market Signal")

c1, c2 = st.columns(2)

c1.metric(
    "Signal",
    signal
)

c2.metric(
    "Confidence",
    f"{confidence:.2f}%"
)


# ================= NEWS FETCHING =================

st.subheader("📰 Recent News")

if "Technology" in selected_name:
    news_query = "Indian technology sector"

elif "Healthcare" in selected_name:
    news_query = "Indian healthcare sector"

elif "Banking" in selected_name:
    news_query = "Indian banking sector"

elif "Bond" in selected_name:
    news_query = "Indian bond market"

elif "Duration" in selected_name:
    news_query = "RBI interest rates"

elif "Corporate" in selected_name:
    news_query = "Indian corporate bond market"

elif "Consumption" in selected_name:
    news_query = "Indian consumer sector"

elif "Contra" in selected_name:
    news_query = "Indian stock market"

else:
    news_query = "Indian mutual fund market"

st.info(
    f"Market news analyzed for: {news_query}"
)

news = get_news(news_query)
if len(news) == 0:

    st.warning(
        "No recent news found."
    )

else:

    for headline in news:
        st.write("•", headline)




# ================= SENTIMENT ANALYSIS =================

sentiment_result = analyze_headlines(news)

sentiment_score = sentiment_result["score"]

if sentiment_score >= 60:
    sentiment_label = "Positive 🟢"

elif sentiment_score >= 40:
    sentiment_label = "Neutral 🟡"

else:
    sentiment_label = "Negative 🔴"


st.subheader(" News Sentiment")

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Positive",
    sentiment_result["positive"]
)

s2.metric(
    "Negative",
    sentiment_result["negative"]
)

s3.metric(
    "Neutral",
    sentiment_result["neutral"]
)

s4.metric(
    "Score",
    f"{sentiment_score}%"
)

st.success(
    f"Overall Sentiment: {sentiment_label}"
)
positive = sentiment_result["positive"]
negative = sentiment_result["negative"]

if positive > negative:
    reason = (
        "Recent debt-market news is largely positive. "
        "Bond market growth, regulatory reforms and "
        "increased investor participation support the outlook."
    )

elif negative > positive:
    reason = (
        "Recent debt-market news is largely negative. "
        "Market uncertainty and adverse developments "
        "may affect investor sentiment."
    )

else:
    reason = (
        "News sentiment is mixed with no strong directional signal."
    )

st.subheader("📌 Why This Prediction?")

st.write(reason)

# ================= AI EXPLANATION =================

#st.subheader("🧠 AI Explanation")

# with st.spinner("Generating explanation..."):

  #  explanation = generate_explanation(
    #    fund_name=selected_name,
     #   prediction=prediction,                                #  the local llm cant be deployed so commented it out
      #  signal=signal,
       # confidence=confidence,
        #news_headlines=news,
        #sentiment_score=sentiment_score
  #  )

#st.write(explanation) 


# ================= NAV CHART =================

st.subheader("📉 NAV Trend Analysis")

df["date"] = pd.to_datetime(df["date"])

fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.plot(
    df["date"],
    df["nav"],
    linewidth=2,
    label="NAV History"
)

ax.scatter(
    df["date"].iloc[-1],
    prediction,
    color="red",
    s=100,
    label="Predicted NAV"
)

ax.set_title(
    "NAV Trend vs Prediction"
)

ax.set_xlabel("Date")

ax.set_ylabel("NAV")

ax.legend()

ax.grid(True)

st.pyplot(fig)