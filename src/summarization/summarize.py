from transformers import pipeline
from tqdm import tqdm
import json

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device= -1)

def summarize_articles(input_path, output_path, batch_size=8, max_input_tokens=1024):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    summarized = []
    valid_indices = []
    valid_texts = []

    for idx, article in enumerate(articles):
        text = article['content']
        if len(text.split()) >= 50:
            valid_indices.append(idx)
            valid_texts.append(text[:max_input_tokens])

    for i in tqdm(range(0, len(valid_texts), batch_size), desc="Summarizing"):
        batch_texts = valid_texts[i:i + batch_size]
        batch_indices = valid_indices[i:i + batch_size]
        try:
            summaries = summarizer(batch_texts, max_length=130, min_length=30, do_sample=False)
            for idx, summary in zip(batch_indices, summaries):
                article = articles[idx].copy()
                article['summary'] = summary['summary_text']
                summarized.append(article)
        except Exception as e:
            print(f"⚠️ Batch {i}-{i+batch_size} failed:", e)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summarized, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(summarized)} summarized articles to {output_path}")