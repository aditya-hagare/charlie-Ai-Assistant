import feedparser

def get_news(topic="technology"):
    url = f"https://news.google.com/rss/search?q={topic}"

    feed = feedparser.parse(url)

    headlines = []

    for entry in feed.entries[:5]:
        headlines.append(entry.title)

    return {
        "topic": topic,
        "headlines": headlines
    }
