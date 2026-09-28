from explanation import generate_explanation

headlines = [
    "SBI Mutual Fund IPO gets SEBI approval",
    "Sebi approves SBI Mutual Fund IPO"
]

result = generate_explanation(
    fund_name="SBI Mutual Fund",
    prediction=19.52,
    signal="Bullish",
    confidence=72,
    news_headlines=headlines,
    sentiment_score=100
)

print(result)