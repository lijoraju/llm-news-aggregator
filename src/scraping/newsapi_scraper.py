import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def fetch_news(query="AI", from_days_ago=1, language='en', page_size=20):
    from_date = (datetime.now() - timedelta(days=from_days_ago)).strftime('%Y-%m-%d')

    response = newsapi.get_everything(
        q=query,
        from_param=from_date,
        language=language,
        sort_by='relevancy',
        page_size=page_size
    )

    articles = response.get('articles', [])
    cleaned_articles = []

    for article in articles:
        cleaned_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'published_at': article['publishedAt'],
            'source': article['source']['name'],
            'content':article['content']
        })

    return cleaned_articles

if __name__=="__main__":
    sample = fetch_news(query="technology")
    for a in sample:
        print(a["title"], "-", a["published_at"])