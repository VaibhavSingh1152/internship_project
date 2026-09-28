from analysis_module.technical_analysis import get_stock_data, calculate_indicators, generate_trend_signal
from news_module.sentiment import analyze_headline


def get_news_sentiment(headlines):
    positive = 0
    negative = 0
    neutral = 0

    for h in headlines:
        result = analyze_headline(h).lower()

        if "positive" in result:
            positive += 1
        elif "negative" in result:
            negative += 1
        else:
            neutral += 1

    if positive > negative:
        return "POSITIVE"
    elif negative > positive:
        return "NEGATIVE"
    else:
        return "NEUTRAL"


def final_decision(tech, news):
    if tech == "BULLISH" and news == "POSITIVE":
        return "STRONG BUY"

    if tech == "BEARISH" and news == "NEGATIVE":
        return "STRONG SELL"

    if tech == "BULLISH" and news == "NEGATIVE":
        return "CAUTION / MIXED SIGNAL"

    if tech == "BEARISH" and news == "POSITIVE":
        return "POSSIBLE REVERSAL"

    return "HOLD / UNCLEAR"


def run(symbol, headlines):
    df = get_stock_data(symbol)
    df = calculate_indicators(df)
    tech_signal = generate_trend_signal(df)

    news_signal = get_news_sentiment(headlines)

    print("\n===== AI FINANCE ENGINE =====")
    print("Symbol:", symbol)
    print("Technical Signal:", tech_signal)
    print("News Signal:", news_signal)

    decision = final_decision(tech_signal, news_signal)

    print("\nFINAL DECISION:", decision)