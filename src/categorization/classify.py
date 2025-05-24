from transformers import pipeline
from tqdm import tqdm
import json

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device= -1)

DEFAULT_LABELS = ["Technology", "Business", "Health", "Sports", 
                  "Science", "Politics", "Entertainment and Celebrity News", "Stock Market and Investments"]

LABEL_MAP = {
    "Technology": "Technology",
    "Business": "Business",
    "Politics": "Politics",
    "Sports": "Sports",
    "Health": "Health",
    "Science": "Science",
    "Entertainment and Celebrity News": "Entertainment",
    "Stock Market and Investments": "Stock Market"
}

def classify_articles(input_path, output_path, candidate_labels=DEFAULT_LABELS, batch_size=8):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    classified = []
    summaries = [article['summary'] for article in articles]
    total = len(summaries)
    
    for i in tqdm(range(0, total, batch_size), desc="Classifying"):
        batch_summaries = summaries[i:i + batch_size]
        try:
            batch_results = classifier(batch_summaries, candidate_labels)
            if isinstance(batch_results, dict):
                batch_results = [batch_results]
            for j, (article, result) in enumerate(zip(articles[i:i+batch_size], batch_results)):
                tagged_article = article.copy()
                tagged_article['category'] = LABEL_MAP[result['labels'][0]]
                classified.append(tagged_article)
        except Exception as e:
            print(f"⚠️ Error classifying batch {i}-{i+batch_size}:", e)
            
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(classified, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(classified)} categorized articles to {output_path}")

