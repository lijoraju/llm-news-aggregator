from newspaper import Article
from tqdm import tqdm
import json

def extract_full_articles(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f :
        articles = json.load(f)
    
    enriched_articles = []

    for article in tqdm(articles):
        url = article['url']
        try:
            news_article = Article(url)
            news_article.download()
            news_article.parse()
            full_text = news_article.text.strip()

            if full_text and len(full_text) > 50:
                article['content'] = full_text
                enriched_articles.append(article)
        
        except Exception as e:
            print(f"Failed to extract {url} - {e}")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched_articles, f, indent=2, ensure_ascii=False)

    print(f"Extracted full content for {len(enriched_articles)} articles.")