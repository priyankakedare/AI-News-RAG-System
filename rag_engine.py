import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

_embedder = None
_collection = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.Client(
            Settings(
                persist_directory="rag_db",
                anonymized_telemetry=False
            )
        )
        _collection = client.get_or_create_collection("news")
    return _collection

def store_articles(articles):
    embedder = get_embedder()
    collection = get_collection()

    docs, ids, metas = [], [], []

    for art in articles:
        docs.append(
            art["title"] + "\n" + art["content"]
        )
        ids.append(art["id_hash"])
        metas.append({"title": art["title"]})

    embeddings = embedder.encode(docs).tolist()

    collection.add(
        documents=docs,
        ids=ids,
        metadatas=metas,
        embeddings=embeddings
    )

def search_articles(query, top_k=5):
    embedder = get_embedder()
    collection = get_collection()

    q_emb = embedder.encode(query).tolist()

    return collection.query(
        query_embeddings=[q_emb],
        n_results=top_k
    )
