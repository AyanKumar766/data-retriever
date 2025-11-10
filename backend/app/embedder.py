"""
Embedder & FAISS index utilities.

- Builds FAISS index from WebItem.text fields.
- Persists index to embeddings/faiss_index/data.index
- Persists mapping of index id -> WebItem.id as numpy array embeddings/faiss_index/ids.npy

Requires: sentence-transformers, faiss-cpu (or faiss)
"""
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sqlmodel import Session, select
from .db import engine
from .models import WebItem
from .crud import get_items_with_text

EMBED_DIR = os.path.join(os.path.dirname(__file__), "..", "embeddings", "faiss_index")
os.makedirs(EMBED_DIR, exist_ok=True)
INDEX_PATH = os.path.join(EMBED_DIR, "data.index")
IDS_PATH = os.path.join(EMBED_DIR, "ids.npy")

# choose a lightweight, quick model
MODEL_NAME = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def build_index(session: Session):
    model = get_model()
    items = get_items_with_text(session)
    texts = []
    ids = []
    for it in items:
        if it.text and len(it.text.strip()) > 20:
            texts.append(it.text)
            ids.append(int(it.id))
    if not texts:
        # create empty index
        print("No texts available to build index.")
        # remove old files if exist
        if os.path.exists(INDEX_PATH):
            os.remove(INDEX_PATH)
        if os.path.exists(IDS_PATH):
            os.remove(IDS_PATH)
        return {"status": "no_texts", "count": 0}

    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))
    faiss.write_index(index, INDEX_PATH)
    np.save(IDS_PATH, np.array(ids, dtype=np.int64))
    return {"status": "built", "count": len(ids)}

def load_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(IDS_PATH):
        return None, None
    index = faiss.read_index(INDEX_PATH)
    ids = np.load(IDS_PATH)
    return index, ids

def query_index(query: str, k: int = 5):
    model = get_model()
    index, ids = load_index()
    if index is None:
        return {"error": "index_not_built"}
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    D, I = index.search(q_emb, k)
    # I is indices into embeddings (0..n-1). map to item ids using ids array.
    hits = []
    for i, dist in zip(I[0], D[0]):
        if i == -1:
            continue
        item_id = int(ids[int(i)])
        hits.append({"item_id": item_id, "score": float(dist)})
    return {"query": query, "results": hits}
