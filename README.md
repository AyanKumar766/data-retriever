 🌐 ***AI Data Retriever***

> **An AI-powered data collection, semantic search, and analysis tool built with FastAPI, SQLite, and FAISS.**  
> Collect, organize, and explore web content intelligently — locally and privately.

## 🧠 Overview

**AI Data Retriever** is an end-to-end Python application that:
- Automatically scrapes content from any website  
- Stores and tracks data locally in a SQLite database  
- Converts text into vector embeddings for **semantic search** using FAISS  
- Provides a clean, fast **web UI** (HTML/CSS/JS served by FastAPI)  

Think of it as your personal **AI-powered web intelligence dashboard** — perfect for research, knowledge management, or building datasets for AI/ML projects.

---

## ✨ Features

| Feature | Description |
|----------|--------------|
| 🧭 **Web Scraper** | Extracts article titles, text, and metadata using BeautifulSoup. |
| 💾 **Local Database (SQLite)** | Stores and tracks all retrieved data securely. |
| 🧠 **Semantic Search Engine (FAISS)** | Search by meaning, not keywords. |
| 🧩 **AI Embeddings** | Uses SentenceTransformers (`all-MiniLM-L6-v2`) for vector representations. |
| 🎨 **Built-in Web UI** | HTML + CSS interface to add URLs, view pages, and perform AI searches. |
| ⚙️ **Offline-Ready** | No external APIs required — runs completely on your machine. |
| 🧱 **Modular Codebase** | Cleanly separated backend, scraper, embedder, and templates. |

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Backend | 🐍 **FastAPI** | API + Template rendering |
| Database | 💾 **SQLite (SQLModel)** | Local structured storage |
| Scraper | 🌐 **Requests + BeautifulSoup** | Web content extraction |
| Embeddings | 🧠 **SentenceTransformers** | Text vectorization |
| Vector Search | ⚡ **FAISS** | Semantic similarity search |
| Frontend | 🎨 **HTML + CSS + JS** | Interactive dashboard |
| Optional | 🧩 **Playwright** | Dynamic site scraping (JS pages) |

---

## 🏗️ Architecture

<img width="924" height="636" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/da193603-acc0-46a0-b3b8-36e029be9873" />



## 🚀 Getting Started

### 🧰 Requirements
- Python **3.9+**
- pip (Python package manager)
- (Optional) Playwright if you want dynamic page scraping

---


## Installation



```bash
  1. Clone the repo:
   git clone https://github.com/yourusername/ai-data-retriever.git
   cd ai-data-retriever

2. Create virtual environment:
   python -m venv .venv
   source .venv/bin/activate

3. Install dependencies:
   pip install -r backend/requirements.txt

4. Run backend:
   uvicorn backend.app.main:app --reload

5. Open in browser:
   http://127.0.0.1:8000
```
    
## Authors

- [@AyanKumar766](https://www.github.com/AyanKumar766)

