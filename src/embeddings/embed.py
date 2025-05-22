from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from pathlib import Path

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faiss.omp_set_num_threads(1)

def build_faiss_index(input_path, index_path="data/processed/articles_faiss.index", metadata_path="data/processed/article_metadata.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    texts = [a["title"] + ". " + a["summary"] for a in articles]
    embeddings = embedder.encode(texts, show_progress_bar=True)

    embedding_dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(embeddings).astype("float32"))

    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, index_path)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"✅ FAISS index saved to {index_path}")
    print(f"✅ Metadata saved to {metadata_path}")