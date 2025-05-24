import re
import json
from bs4 import BeautifulSoup
from pathlib import Path
import hashlib

def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()

def normalize_text(text):
    if not text:
        return ""
    text = clean_html(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.(?=[A-Za-z])', '. ', text)
    return text.strip()

def preprocess_articles(input_path, output_path, min_words=150):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    cleaned_articles = []
    seen_titles = set()
    seen_contents = set()

    for article in articles:
        content = normalize_text(article['content'])
        title = normalize_text(article['title'])
        if content and len(content.split()) >= min_words:
            title_key = title.lower().strip()
            content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
            if (title_key not in seen_titles) and (content_hash not in seen_contents):
                seen_titles.add(title_key)
                seen_contents.add(content_hash)
                cleaned_articles.append({
                    "title": title,
                    "content": content, 
                    "published_at": article.get("published_at"),
                    "source": article.get("source"),
                    "url": article.get("url")
                })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, indent=2, ensure_ascii=False)

    print(f"Preprocessed {len(cleaned_articles)} articles saved to {output_path}")