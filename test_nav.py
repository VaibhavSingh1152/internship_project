from news_module.sentiment import analyze_headline

headline = input("Enter headline: ")

result = analyze_headline(headline)

print("Sentiment:", result)