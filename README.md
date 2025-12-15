# 📰 AI News RAG System

An AI-powered web application that fetches real-time news, summarizes articles using a Large Language Model (LLM), and answers user questions using **Retrieval-Augmented Generation (RAG)** to ensure accurate and grounded responses.

---

## 🔍 Problem Statement
Reading full news articles daily is time-consuming, and traditional keyword-based search often fails to give precise answers.  
This project solves that by:
- Automatically summarizing news
- Allowing users to ask questions in natural language
- Ensuring answers are based only on the news content (no hallucination)

---

## 🚀 Features
- Fetches real-time news using RSS feeds
- AI-based news summarization (TL;DR + bullet points)
- Semantic search using embeddings
- RAG-based question answering
- Hallucination control (“Not mentioned” responses)
- Debug mode to inspect retrieved documents
- Clean Streamlit web interface

---

## 🧠 How the System Works (End-to-End)

1. News articles are fetched from RSS feeds (BBC, NYT, etc.)
2. Article text is cleaned and processed
3. Articles are summarized using a pre-trained LLM
4. Articles are converted into embeddings
5. Embeddings are stored in a ChromaDB vector database
6. User questions retrieve relevant articles (semantic search)
7. The LLM answers using **only retrieved context**

---

## 🤖 Models Used

### 1. Large Language Model (LLM)
- **Groq-hosted LLM (`compound-beta`)**
- Used for:
  - News summarization
  - Answer generation in RAG

### 2. Embedding Model
- **SentenceTransformer: `all-MiniLM-L6-v2`**
- Used to convert text into numerical vectors for semantic search

> No model training was done — only pre-trained models were used (industry-standard practice).

---

## 🛡️ RAG Safety & Hallucination Control
The system strictly follows these rules:
- Answers are generated **only from retrieved news articles**
- If the answer is not present, the system responds with:
  
  **“This information is not mentioned in the news.”**

This ensures reliable and trustworthy outputs.

---

## 🧪 Example Questions

- Who were the victims of the Bondi shooting?
- What is SpaceX’s current valuation and why is it significant?
- What progress was made in Ukraine ceasefire talks?
- What penalties will states face if they ignore the AI executive order?

(Last question correctly returns *“Not mentioned”*.)

---

## 🧰 Tech Stack
- Python
- Streamlit
- Groq LLM (OpenAI-compatible API)
- Sentence Transformers
- ChromaDB (Vector Database)
- Feedparser (RSS)
- BeautifulSoup
- Git & GitHub
