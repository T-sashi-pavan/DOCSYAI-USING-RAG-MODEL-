# 📄 PDF Q&A RAG Backend

A powerful **Retrieval-Augmented Generation (RAG)** backend API that enables intelligent question-answering over PDF documents. Built with FastAPI and optimized for low-memory cloud deployments (500MB).

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🚀 **Fast PDF Processing** - Upload and process PDFs with streaming for memory efficiency
- 🤖 **Intelligent Q&A** - Ask questions and get accurate answers based on PDF content
- 🔄 **Streaming Responses** - Real-time streaming answers for better UX
- 💾 **Vector Storage** - Supabase-powered vector store for efficient semantic search
- 🧠 **Smart Fallback** - Falls back to general knowledge when PDF doesn't contain relevant info
- 📊 **Health Monitoring** - Built-in health checks and statistics endpoints
- 🐳 **Docker Ready** - Optimized Dockerfile for cloud deployment

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

## 📋 Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com/) - For LLM inference
- [HuggingFace API Key](https://huggingface.co/settings/tokens) - For embeddings
- [Supabase Account](https://supabase.com/) - For vector storage

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/adityacodeverse-stack/ragbackend.git
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
# LLM Provider
GROQ_API_KEY=gsk_your_groq_api_key_here

# Embeddings
HUGGINGFACE_API_KEY=hf_your_huggingface_token_here

# Vector Store
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:10000`

---

## 📡 API Endpoints

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

## 📝 Usage Examples

### Upload a PDF

```bash
curl -X POST "http://localhost:10000/upload" \
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
curl -X POST "http://localhost:10000/ask" \
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
curl -X POST "http://localhost:10000/ask-stream" \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the key points"}'
```

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t pdf-qa-backend .
```

### Run the Container

```bash
docker run -d \
  -p 10000:10000 \
  -e GROQ_API_KEY=your_key \
  -e HUGGINGFACE_API_KEY=your_key \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_ANON_KEY=your_key \
  pdf-qa-backend
```

---

## ☁️ Cloud Deployment

### Render.com

This project includes a `render.yaml` for easy deployment on Render:

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy!

### Environment Variables Required

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key for LLM inference |
| `HUGGINGFACE_API_KEY` | HuggingFace token for embeddings |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anonymous key |

---

## 📁 Project Structure

```
ragbackend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── render.yaml             # Render.com deployment config
├── deploy.sh               # Deployment helper script
├── src/
│   ├── __init__.py
│   ├── rag_system.py       # Main RAG orchestrator
│   ├── pdf_loader.py       # PDF text extraction
│   ├── text_chunker.py     # Text splitting logic
│   ├── vector_store.py     # Supabase vector storage
│   ├── embeddings.py       # HuggingFace embeddings
│   ├── llm_manager.py      # Groq LLM integration
│   ├── cache_manager.py    # Caching utilities
│   └── memory_monitor.py   # Memory monitoring
├── test_basic.py           # Basic tests
├── test_groq_models.py     # Groq model tests
├── test_hf_token.py        # HuggingFace token tests
└── verify_setup.py         # Setup verification script
```

---

## ⚡ Performance Optimizations

This backend is optimized for **500MB memory environments**:

- **Streaming PDF Processing** - Pages processed one at a time
- **Batch Chunk Processing** - Chunks added in small batches with garbage collection
- **Async Operations** - Non-blocking I/O for better concurrency
- **Background Processing** - PDF ingestion runs in background tasks
- **Efficient Embeddings** - API-based embeddings (no local models)

---

## 🔧 Configuration

Key configuration options in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `chunk_size` | 300 | Characters per chunk |
| `top_k` | 5 | Number of chunks to retrieve |
| `threshold` | 0.7 | Relevance threshold for filtering |
| `llm_model` | `llama-3.1-8b-instant` | Groq model for generation |

---

## 🧪 Testing

Run the verification scripts:

```bash
# Verify setup
python verify_setup.py

# Test basic functionality
python test_basic.py

# Test Groq models
python test_groq_models.py

# Test HuggingFace token
python test_hf_token.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [HuggingFace](https://huggingface.co/) - AI models and embeddings
- [Supabase](https://supabase.com/) - Open source Firebase alternative

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/adityacodeverse-stack">Aditya</a>
</p>
