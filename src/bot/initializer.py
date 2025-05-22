from pathlib import Path
from pipeline.refresh_pipeline import run_pipeline

def is_faiss_index_present():
    return (
        Path("data/processed/articles_faiss.index").exists() and
        Path("data/processed/article_metadata.json").exists()
    )

def initialize_pipeline():
    if not is_faiss_index_present():
        print("⚠️ FAISS index not found. Running pipeline...")
        run_pipeline()

if __name__ == "__main__":
    initialize_pipeline()