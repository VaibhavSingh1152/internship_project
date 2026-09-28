from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_headlines(headlines):

    results = []

    positive = 0
    negative = 0
    neutral = 0

    for headline in headlines:

        score = analyzer.polarity_scores(headline)["compound"]

        if score >= 0.05:
            sentiment = "Positive"
            positive += 1

        elif score <= -0.05:
            sentiment = "Negative"
            negative += 1

        else:
            sentiment = "Neutral"
            neutral += 1

        results.append({
            "headline": headline,
            "sentiment": sentiment,
            "score": score
        })

    total = len(headlines)

    sentiment_score = round((positive / total) * 100, 2)

    return {
        "headlines": results,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "score": sentiment_score
    }