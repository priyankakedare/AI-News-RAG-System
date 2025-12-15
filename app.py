import streamlit as st
import feedparser
import hashlib
from bs4 import BeautifulSoup

from summarizer import summarize_article, rag_answer
from rag_engine import store_articles

st.set_page_config("Daily News Bot", layout="wide")
st.title("📰 AI Daily News Summarizer with RAG")

# ---------------- Session State ----------------
if "articles" not in st.session_state:
    st.session_state.articles = []

if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if "fetched" not in st.session_state:
    st.session_state.fetched = False

# ---------------- RSS Feeds ----------------
FEEDS = {
    "World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
}

topic = st.selectbox("Select Topic", FEEDS.keys())

# ---------------- Fetch News ----------------
if st.button("Fetch News"):
    feed = feedparser.parse(FEEDS[topic])
    articles = []

    for entry in feed.entries[:3]:
        text = BeautifulSoup(entry.summary, "html.parser").get_text()
        aid = hashlib.md5(entry.link.encode()).hexdigest()

        articles.append({
            "title": entry.title,
            "content": text,
            "id_hash": aid
        })

    st.session_state.articles = articles
    st.session_state.fetched = True

    store_articles(articles)

    summaries = {}
    for art in articles:
        summaries[art["id_hash"]] = summarize_article(
            art["title"], art["content"], art["id_hash"]
        )

    st.session_state.summaries = summaries

# ---------------- Show News ----------------
if st.session_state.fetched:
    st.subheader("📰 Latest News")

    for art in st.session_state.articles:
        st.markdown(f"### {art['title']}")
        st.code(st.session_state.summaries.get(art["id_hash"], ""))

# ---------------- RAG Section ----------------
st.divider()
st.subheader("🧠 Ask the News (RAG)")

question = st.text_input("Ask a question based on the news")

if st.button("Ask"):
    if question.strip():
        answer, sources, docs = rag_answer(question)
        st.write(answer)

        if sources:
            st.subheader("Sources")
            for s in set(sources):
                st.write("•", s)

        if st.checkbox("Show retrieved documents (debug)"):
            st.subheader("Retrieved Context")
            for i, d in enumerate(docs, 1):
                st.markdown(f"**Doc {i}**")
                st.text(d[:800])
    else:
        st.warning("Please enter a question.")
