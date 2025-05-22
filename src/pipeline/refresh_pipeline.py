import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraping.newsapi_scraper import fetch_news
from scraping.article_extractor import extract_full_articles
from preprocessing.preprocess import preprocess_articles
from summarization.summarize import summarize_articles
from categorization.classify import classify_articles
from embeddings.embed import build_faiss_index


def run_pipeline():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    raw_file = f"data/raw/newsapi_{date_str}.json"
    fulltext_file = f"data/raw/fulltext_{date_str}.json"
    cleaned_file = f"data/processed/cleaned_{date_str}.json"
    summarized_file = f"data/processed/summarized_{date_str}.json"
    tagged_file = f"data/processed/tagged_{date_str}.json"
    
    _ = fetch_news(query="AI", max_pages=5, save=True)
    extract_full_articles(raw_file, fulltext_file)
    preprocess_articles(fulltext_file, cleaned_file)
    summarize_articles(cleaned_file, summarized_file)
    classify_articles(summarized_file, tagged_file)
    build_faiss_index(tagged_file)


if __name__ == "__main__":
    run_pipeline()
