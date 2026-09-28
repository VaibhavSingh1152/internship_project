from fetch_news import get_news
from sentiment import analyze_headlines

news = get_news("SBI Mutual Fund")

result = analyze_headlines(news)

print("\nSentiment Summary")
print("---------------------")

print("Positive:", result["positive"])
print("Negative:", result["negative"])
print("Neutral :", result["neutral"])
print("Score   :", result["score"], "%")

print("\nDetailed Results\n")

for item in result["headlines"]:
    print(item["sentiment"], "-", item["headline"])