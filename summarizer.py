import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from rag_engine import search_articles

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("GROQ_MODEL", "compound-beta")
CACHE_FILE = "summary_cache.json"

# ---------------- Cache ----------------
def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

# ---------------- Summarizer ----------------
def summarize_article(title, content, article_id):
    cache = load_cache()
    if article_id in cache:
        return cache[article_id]

    prompt = f"""
You are a news summarizer.

Give:
1. One-line TL;DR
2. 3–5 bullet points

Title: {title}
Content:
{content}
"""

    resp = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=300,
        temperature=0.2
    )

    summary = resp.output_text
    cache[article_id] = summary
    save_cache(cache)
    time.sleep(0.3)

    return summary

# ---------------- RAG Answer ----------------
def rag_answer(question):
    results = search_articles(question)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    if not docs:
        return "No relevant news found.", [], []

    context = ""
    sources = []

    for i, doc in enumerate(docs):
        context += f"[DOC {i+1}]\n{doc}\n\n"
        if i < len(metas):
            sources.append(metas[i].get("title", "Unknown"))

    rag_prompt = f"""
You are an AI assistant answering questions ONLY using the provided news context.

RULES:
- Use ONLY the information in the context.
- If the answer is NOT present, say exactly:
  "This information is not mentioned in the news."
- Do NOT guess.
- Do NOT add outside knowledge.

Context:
{context}

Question:
{question}

Answer clearly.
"""

    resp = client.responses.create(
        model=MODEL,
        input=rag_prompt,
        max_output_tokens=300,
        temperature=0.2
    )

    answer = resp.output_text.strip()
    if not answer:
        answer = "This information is not mentioned in the news."

    return answer, sources, docs
