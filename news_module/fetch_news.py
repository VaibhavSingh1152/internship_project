import feedparser


def get_news(query, max_news=10):

    search_query = query.replace(" ", "+")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={search_query}+when:30d&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    headlines = []

    seen = set()

    for entry in feed.entries:

        title = entry.title.strip()

        # Remove duplicate headlines
        if title not in seen:

            seen.add(title)
            headlines.append(title)

        if len(headlines) >= max_news:
            break

    return headlines


if __name__ == "__main__":

    news = get_news("RBI interest rates")

    print("\nLATEST NEWS\n")

    for n in news:
        print("-", n)