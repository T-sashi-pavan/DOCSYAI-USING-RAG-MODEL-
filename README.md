# DocsyAI - RAG Document Intelligence

A production-ready **Retrieval-Augmented Generation (RAG)** system for intelligent document question-answering. Upload PDFs and get instant, accurate answers powered by AI.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Deployed](https://img.shields.io/badge/Status-Live-success)

---

## Features

- **Fast PDF Processing** - Streaming upload and processing optimized for 512MB memory environments
- **Intelligent Q&A** - Context-aware answers from your documents using advanced RAG techniques
- **Real-time Responses** - Streaming LLM responses for better user experience
- **Vector Search** - Supabase pgvector for efficient semantic similarity search
- **Smart Fallback** - Answers general questions when content not found in documents
- **Production Ready** - Currently deployed and serving 2,600+ document chunks
- **Session Management** - Persistent chat history with localStorage

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Server                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────────┐    ┌──────────────────┐     │
│   │  Upload  │───▶│  PDF Loader  │───▶│   Text Chunker   │     │
│   │   API    │    │  (Streaming) │    │   (300 chars)    │     │
│   └──────────┘    └──────────────┘    └────────┬─────────┘     │
│                                                 │               │
│   ┌──────────┐    ┌──────────────┐    ┌────────▼─────────┐     │
│   │   Ask    │◀──▶│  LLM Manager │◀──▶│   Vector Store   │     │
│   │   API    │    │    (Groq)    │    │   (Supabase)     │     │
│   └──────────┘    └──────────────┘    └──────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com/) - LLM inference (llama-3.1-8b-instant)
- [Cohere API Key](https://cohere.com/) - Text embeddings (embed-english-light-v3.0)
- [Supabase Account](https://supabase.com/) - pgvector database

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/T-sashi-pavan/DOCSYAI-USING-RAG-MODEL-.git
cd ragbackend
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Python Version
PYTHON_VERSION=3.11.0

# LLM Provider
GROQ_API_KEY=your_groq_api_key_here

# Embeddings
COHERE_API_KEY=your_cohere_api_key_here

# Vector Store
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8001`

### 5. Access the Frontend

Open `static/index.html` in your browser or access it at:
- **Production**: https://docsyai-using-rag-model.onrender.com
- **Local**: http://localhost:8001

---

## API Endpoints

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API root - returns status |
| `GET` | `/health` | Detailed health check with environment status |
| `GET` | `/stats` | Get system statistics (document count, etc.) |

### Document Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload and process a PDF file |
| `DELETE` | `/clear` | Clear all documents from database |

### Question & Answer

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ask` | Ask a question (standard response) |
| `POST` | `/ask-stream` | Ask a question (streaming response) |

---

## Usage Examples

### Upload a PDF

```bash
curl -X POST "http://localhost:8001/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "processing",
  "filename": "document.pdf",
  "message": "PDF is being processed. Query the /stats endpoint to check progress."
}
```

### Ask a Question

```bash
curl -X POST "http://localhost:8001/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of the document?",
    "top_k": 5,
    "threshold": 0.7
  }'
```

**Response:**
```json
{
  "answer": "The document discusses...",
  "sources": [
    {
      "text": "relevant chunk...",
      "page": 1,
      "distance": 0.45
    }
  ],
  "mode": "pdf"
}
```

### Streaming Response

```bash
curl -X POST "http://localhost:8001/ask-stream" \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the key points"}'
```

---

## Deployment

### Render.com (Production)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables:
   - `PYTHON_VERSION=3.11.0`
   - `GROQ_API_KEY`
   - `COHERE_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
4. Deploy automatically on push

Current production deployment: https://docsyai-using-rag-model.onrender.com

---

## Project Structure

```
ragbackend/
├── main.py                 # FastAPI server
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── render.yaml             # Render deployment
├── static/
│   └── index.html          # Frontend UI
└── src/
    ├── rag_system.py       # RAG orchestrator
    ├── pdf_loader.py       # PDF processing
    ├── text_chunker.py     # Text splitting
    ├── vector_store.py     # Supabase storage
    ├── embeddings.py       # Cohere embeddings
    ├── llm_manager.py      # Groq LLM
    ├── cache_manager.py    # Caching
    └── memory_monitor.py   # Memory tracking
```

---

## Performance

Optimized for **512MB memory environments** (Render free tier):

- Memory usage: ~71MB baseline (86% under limit)
- Streaming PDF processing with garbage collection
- API-based embeddings (no heavy local models)
- Async FastAPI for concurrent requests
- Background task processing
- Currently serving 2,600+ document chunks

---

## Configuration

Key configuration options in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `chunk_size` | 300 | Characters per chunk |
| `top_k` | 5 | Number of chunks to retrieve |
| `threshold` | 0.7 | Relevance threshold for filtering |
| `llm_model` | `llama-3.1-8b-instant` | Groq model for generation |

---

## Technology Stack

- **Backend**: FastAPI, Python 3.11
- **LLM**: Groq (llama-3.1-8b-instant)
- **Embeddings**: Cohere (embed-english-light-v3.0, 384 dimensions)
- **Database**: Supabase pgvector
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Render.com

---

## License

MIT License - feel free to use this project for your own purposes.
