import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from pathlib import Path

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

def save_articles(articles, output_path="data/raw/newsapi_articles.json"):
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def fetch_news(query="top headlines", from_days_ago=1, language='en', page_size=20, max_pages=3, save=False):
    from_date = (datetime.now() - timedelta(days=from_days_ago)).strftime('%Y-%m-%d')
    all_articles = []

    for page in range(1, max_pages + 1):
        try:
            response = newsapi.get_everything(
                q=query,
                from_param=from_date,
                language=language,
                sort_by='relevancy',
                page=page,
                page_size=page_size
            )
            # response = newsapi.get_top_headlines(
            #     language=language,
            #     page_size=page_size,
            #     page=page
            # )

            articles = response.get('articles', [])
            if not articles:
                break

            for article in articles:
                all_articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'published_at': article['publishedAt'],
                    'source': article['source']['name'],
                    'content':article['content']
                })
        except Exception as e:
            print(f"Error on page {page}: {e}")
    
    if save:
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        with open(f"data/raw/newsapi_{date_str}.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)

    return all_articles
