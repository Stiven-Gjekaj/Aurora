<div align="center">

# ✦ Aurora

### Personal AI Research Assistant

*Search · Remember · Connect*

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-local_memory-003B57?style=flat-square&logo=sqlite&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-knowledge_graph-FF7043?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-llama3-black?style=flat-square&logo=ollama&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22C55E?style=flat-square)

</div>

---

Aurora is a local-first research assistant. Give it a query and it pulls from **Wikipedia** and **arXiv**, ranks and summarizes the results, then persists everything to a **SQLite knowledge base** — building a graph of how topics relate over time.

---

## ⚡ Features

| | |
|---|---|
| 🔍 **Multi-source retrieval** | Wikipedia + arXiv in a single search |
| 🧠 **AI summarization** | Local LLM via Ollama (`llama3`), graceful fallback if unavailable |
| 🗄️ **Persistent memory** | Topics, content, and named relationships stored across sessions |
| 🕸️ **Knowledge graph** | Directed graph with BFS traversal and PNG export |

---

## 🚀 Setup

```bash
# 1. Clone & enter
git clone <repo-url> && cd Aurora

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Start Ollama for AI summaries
ollama pull llama3
ollama serve
```

> Ollama is **optional** — Aurora falls back to plain-text truncation if it's not running.

---

## 🖥️ Usage

```bash
# Research a topic — fetches, ranks, summarizes, and stores results
python main.py --query "quantum computing"

# Explore stored topics and their relationships
python main.py --explore

# Export the knowledge graph as a PNG image
python main.py --visualize
```

**Example output:**

```
Research Results for 'quantum computing':
==================================================
1. Quantum computing
   Summary: Quantum computing uses quantum-mechanical phenomena such as...
   Relevance: 6

2. Quantum supremacy
   Summary: Quantum supremacy is the goal of demonstrating that a...
   Relevance: 4
```

---

## 🗂️ Project Structure

```
Aurora/
├── main.py              ← CLI entry point & orchestrator
├── retrieval_system.py  ← Wikipedia, arXiv, web scraping
├── memory_system.py     ← SQLite persistence layer
├── knowledge_graph.py   ← NetworkX graph, BFS, PNG export
├── ai_assistant.py      ← Ollama summarization & ranking
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Library | Role |
|---|---|
| [`wikipedia`](https://pypi.org/project/wikipedia/) | Wikipedia article retrieval |
| [`arxiv`](https://github.com/lukasschwab/arxiv.py) | Academic paper search |
| [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) | Web page scraping |
| [`networkx`](https://networkx.org) | Knowledge graph structure & traversal |
| [`matplotlib`](https://matplotlib.org) | Graph visualization |
| [`ollama`](https://ollama.com) | Local LLM inference |
| `sqlite3` | Persistent memory (stdlib) |

---

## 📋 Requirements

- **Python** 3.9+
- **Ollama** *(optional)* — [ollama.com](https://ollama.com)

---

<div align="center">
  <sub>Built with Python · Runs entirely local · No API keys required</sub>
</div>
