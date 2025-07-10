# AI News Generation Backend

This project is a backend system for fetching, summarizing, and interacting with the latest news and stock updates using **LangGraph**, **FastAPI**, and a set of AI tools exposed via an **MCP (Multi-Component Protocol) server**.

It supports:
- Automatic news scraping and summarization
- Semantic search over news using vector similarity
- Query-based chat using an LLM + external tools like Tavily and Supabase
- API endpoints for frontend integration

---

## Features

✅ Scrape and summarize real-time news  
✅ Save summaries to vector DB (Supabase) for semantic search  
✅ Use agents to dynamically choose the right tools  
✅ FastAPI-powered backend for client communication  
✅ LangGraph orchestrates dynamic flows based on user input  

---

## Technologies Used

| Tool/Tech         | Purpose |
|------------------|---------|
| **LangGraph**     | Stateful workflow engine to handle dynamic logic (scraper vs agent query) |
| **FastAPI**       | RESTful API server |
| **Supabase + pgvector** | Vector database to store and retrieve similar news articles |
| **Tavily API**    | Web search API for fetching latest stock or event-specific news |
| **MCP Server**    | Modular tool hosting system for search, summarization, and semantic tools |
| **LLM Agent**     | Uses `ToolCallingAgent` (e.g., with GPT, Ollama) to dynamically use tools |
| **SentenceTransformer** | Embedding model for storing news vectors |
| **Uvicorn**       | ASGI server for FastAPI |
| **LangChain tools** | Tool wrappers and agents with memory support |

---

## Project Structure
  To be added
  
## Running the Backend

### 1. Setup virtualenv and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Configure and activate ollama/ other LLM models 

### 3. Start the MCP server 

```bash
python api/mcp_server.py
```

### 4. Run the FastAPI app (add port accordingly)

```bash
uvicorn endpoints:app --reload --port 8080 
```
### Running the frontend
  To be added
