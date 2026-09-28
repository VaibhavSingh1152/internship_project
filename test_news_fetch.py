import feedparser

symbol = input("Enter stock symbol: ").upper()

url = f"https://news.google.com/rss/search?q={symbol}+stock"

feed = feedparser.parse(url)

entries = feed.entries

print("Number of headlines:", len(entries))

if len(entries) == 0:
    print("\nNo news found.")
else:
    for news in entries[:5]:
        print("\nHeadline:")
        print(news.title)