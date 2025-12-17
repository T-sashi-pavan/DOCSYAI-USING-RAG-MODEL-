# DocsyAI - RAG Document Intelligence 🤖

> **Transform your PDFs into intelligent conversations!** Upload any document and ask questions to get instant, accurate answers powered by AI.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Deployed](https://img.shields.io/badge/Status-Live-success)

---

## 📊 System Architecture

<div align="center">
  <img src="./Gemini_Generated_Image_cx5kz7cx5kz7cx5k.png" alt="DocsyAI RAG System Workflow Diagram" width="800"/>
  <p><em>Complete RAG workflow from PDF upload to intelligent answer generation</em></p>
</div>

**How It Works:**

1. **📤 Upload PDF** → User uploads a document through the web interface
2. **📄 Extract Text** → Backend extracts and processes text from PDF
3. **✂️ Smart Chunking** → Text is split into meaningful 300-character chunks
4. **🧠 Generate Embeddings** → Cohere API converts chunks into vector embeddings
5. **💾 Store Vectors** → Embeddings saved in Supabase pgvector database
6. **❓ User Asks Question** → Question is converted to vector embedding
7. **🔍 Semantic Search** → System finds most relevant chunks using similarity
8. **🤖 AI Response** → Groq LLM generates human-like answer from context
9. **✅ Get Answer** → User receives accurate, context-aware response

---

## ✨ Features

## ✨ Features

✅ **Fast PDF Processing** - Streaming upload and processing optimized for 512MB memory environments

✅ **Intelligent Q&A** - Context-aware answers from your documents using advanced RAG techniques

✅ **Real-time Responses** - Streaming LLM responses for better user experience

✅ **Vector Search** - Supabase pgvector for efficient semantic similarity search

✅ **Smart Fallback** - Answers general questions when content not found in documents

✅ **Production Ready** - Currently deployed and serving 2,600+ document chunks

✅ **Session Management** - Persistent chat history with localStorage

✅ **Mobile Responsive** - Works perfectly on phones, tablets, and desktops

---

## 🎯 What is RAG? (For Beginners)

**RAG** stands for **Retrieval-Augmented Generation**. Think of it as giving an AI assistant a library card!

### Traditional AI Problem:
- Regular AI chatbots (like ChatGPT) only know what they were trained on
- They can't access your specific documents
- They might give outdated or generic answers

### RAG Solution:
- **Retrieval**: Finds relevant information from YOUR documents
- **Augmented**: Adds this information to the AI's context
- **Generation**: AI creates answers based on YOUR data

### Real-World Example:
Imagine you have a 500-page company handbook. Instead of reading the entire thing:
1. You ask: "What is the vacation policy?"
2. RAG finds the exact pages about vacation
3. AI reads only those pages and answers your question
4. You get accurate info in seconds instead of hours!

---

## 🚀 Quick Start (Step-by-Step for Beginners)

### Step 1: Get Your Free API Keys

You'll need 3 free accounts (takes 5 minutes):

#### 1️⃣ Groq (AI Brain)
1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up with Google/Email
3. Click "API Keys" → "Create API Key"
4. Copy the key (looks like: `gsk_...`)

#### 2️⃣ Cohere (Text Understanding)
1. Go to [https://cohere.com/](https://cohere.com/)
2. Sign up for free
3. Go to Dashboard → API Keys
4. Copy your key (looks like: `dWSg...`)

#### 3️⃣ Supabase (Database)
1. Go to [https://supabase.com/](https://supabase.com/)
2. Create new project (free tier)
3. Wait 2 minutes for setup
4. Go to Settings → API
5. Copy "Project URL" and "anon public" key

### Step 2: Download the Code

```bash
# Open your terminal/command prompt and run:
git clone https://github.com/T-sashi-pavan/DOCSYAI-USING-RAG-MODEL-.git
cd ragbackend
```

### Step 3: Install Python (If You Don't Have It)

- Download Python 3.11 from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation!

### Step 4: Set Up the Project

```bash
# Create a virtual environment (isolated Python workspace)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 5: Add Your API Keys

Create a file named `.env` in the `ragbackend` folder and paste this:

```env
PYTHON_VERSION=3.11.0

# Paste your Groq API key here (from Step 1.1)
GROQ_API_KEY=gsk_your_actual_key_here

# Paste your Cohere API key here (from Step 1.2)
COHERE_API_KEY=your_actual_key_here

# Paste your Supabase details here (from Step 1.3)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_actual_anon_key_here
```

### Step 6: Run the Application

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://localhost:8001
INFO:     Application startup complete
```

### Step 7: Open in Browser

1. **Local**: Go to `http://localhost:8001` in your browser
2. **Live Demo**: Visit https://docsyai-using-rag-model.pages.dev
3. You'll see the DocsyAI interface!

### Step 8: Try It Out!

1. Click "Upload PDF Document"
2. Select any PDF file from your computer
3. Wait for "Processing complete" message
4. Type a question about the PDF
5. Click "Send" and watch the AI answer!

---

## 🏗️ Technical Architecture (For Developers)

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

---

## 📡 API Endpoints (For Developers)

### Health & Status

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/` | API root status | `curl http://localhost:8001/` |
| `GET` | `/health` | Detailed health check | `curl http://localhost:8001/health` |
| `GET` | `/stats` | Document count stats | `curl http://localhost:8001/stats` |

### Document Operations

| Method | Endpoint | Description | What It Does |
|--------|----------|-------------|--------------|
| `POST` | `/upload` | Upload PDF file | Processes and stores your PDF |
| `DELETE` | `/clear` | Clear database | Removes all documents |

### Question & Answer

| Method | Endpoint | Description | What It Does |
|--------|----------|-------------|--------------|
| `POST` | `/ask` | Ask a question | Get answer from your PDFs |
| `POST` | `/ask-stream` | Streaming response | Get real-time answer (word-by-word) |

---

## 💡 Usage Examples

### Example 1: Upload a PDF (Using Command Line)

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

### Example 2: Ask a Question (Using Command Line)

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
  "answer": "The document discusses machine learning techniques...",
  "sources": [
    {
      "text": "relevant chunk from your PDF...",
      "page": 1,
      "distance": 0.45
    }
  ],
  "mode": "pdf"
}
```

### Example 3: Using the Web Interface (Easiest!)

1. **Open Browser**: Go to `http://localhost:8001`
2. **Upload PDF**: Click the upload button and select your PDF
3. **Wait**: You'll see "Processing..." then "Complete!"
4. **Ask Questions**: Type your question and click Send
5. **Get Answers**: AI will respond based on your document!

---

## 🚀 Deployment Guide


### Deploy to Google Cloud Platform

For advanced users who want more control:

1. Create a GCP account and enable billing
2. Install Google Cloud CLI
3. Create App Engine application
4. Deploy using `gcloud app deploy`

[Detailed GCP Guide](https://cloud.google.com/appengine/docs/standard/python3/quickstart)

---

## 📁 Project Structure (What Each File Does)

```
ragbackend/
├── main.py                 # 🚀 Main server file (run this to start!)
├── config.py               # ⚙️ Settings and configuration
├── requirements.txt        # 📦 List of Python packages needed
├── render.yaml             # ☁️ Render deployment config
├── .env                    # 🔐 Your secret API keys (YOU create this)
│
├── static/
│   └── index.html          # 🎨 The web interface you see in browser
│
└── src/
    ├── rag_system.py       # 🧠 Main brain - coordinates everything
    ├── pdf_loader.py       # 📄 Reads and extracts text from PDFs
    ├── text_chunker.py     # ✂️ Splits text into smaller pieces
    ├── vector_store.py     # 💾 Saves/retrieves from Supabase
    ├── embeddings.py       # 🔢 Converts text to numbers (vectors)
    ├── llm_manager.py      # 🤖 Talks to Groq AI
    ├── cache_manager.py    # ⚡ Speeds things up with caching
    └── memory_monitor.py   # 📊 Tracks memory usage
```

### What Happens When You Upload a PDF?

1. `pdf_loader.py` extracts the text
2. `text_chunker.py` splits it into 300-character pieces
3. `embeddings.py` converts each piece to vectors (using Cohere)
4. `vector_store.py` saves vectors to Supabase
5. You're ready to ask questions!

### What Happens When You Ask a Question?

1. `embeddings.py` converts your question to a vector
2. `vector_store.py` finds similar vectors in database
3. `rag_system.py` gets the relevant text chunks
4. `llm_manager.py` sends chunks + question to Groq AI
5. AI generates answer based on your document!

---

## ⚡ Performance & Optimization

**Built for Efficiency:**

✅ **Memory Optimized**: Uses only ~71MB (86% under 512MB limit!)
- Streaming PDF processing (one page at a time)
- Automatic garbage collection
- No heavy local models

✅ **Fast Responses**: 
- Async FastAPI for concurrent requests
- API-based embeddings (no local loading)
- Background task processing

✅ **Scalable**:
- Currently serving **2,600+ document chunks**
- Can handle multiple users simultaneously
- Cloudflare Pages for static content

### Why It's Fast:

| Traditional Approach | Our RAG Approach |
|---------------------|------------------|
| Load entire 500-page PDF into memory | Process 1 page at a time |
| Search through whole document | Search only relevant chunks |
| Use 2GB+ local AI model | Use API (0 local storage) |
| Takes 30+ seconds | Takes 2-5 seconds |

---

## ⚙️ Configuration (Advanced Settings)

Edit `config.py` to customize behavior:

| Setting | Default | What It Does | When to Change |
|---------|---------|--------------|----------------|
| `chunk_size` | 300 | Characters per chunk | Increase for longer context |
| `chunk_overlap` | 50 | Overlapping characters | Increase to avoid cutting sentences |
| `top_k` | 5 | Number of chunks to retrieve | Increase for more context |
| `threshold` | 0.7 | Relevance score minimum | Lower to get more (but less relevant) results |
| `llm_model` | `llama-3.1-8b-instant` | Groq model name | Change for different AI models |

### Example Configuration Changes:

**For Technical Documents (more context needed):**
```python
chunk_size = 500  # Longer chunks
top_k = 8         # More chunks retrieved
```

**For Quick Answers (faster responses):**
```python
chunk_size = 200  # Shorter chunks
top_k = 3         # Fewer chunks
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework (fast and easy)
- **Python 3.11** - Programming language
- **Uvicorn** - Lightning-fast ASGI server

### AI & Machine Learning
- **Groq** - Ultra-fast LLM inference (llama-3.1-8b-instant model)
- **Cohere** - Text embeddings API (embed-english-light-v3.0, 384 dimensions)
- **RAG Architecture** - Retrieval-Augmented Generation for accuracy

### Database
- **Supabase** - PostgreSQL database with pgvector extension
- **pgvector** - Vector similarity search (finds similar text chunks)

### Frontend
- **HTML5** - Modern web structure
- **CSS3** - Beautiful, responsive styling
- **Vanilla JavaScript** - No frameworks, just pure JS
- **Font Awesome** - Beautiful icons

### Deployment
- **Render.com** - Backend hosting (512MB free tier)
- **Cloudflare Pages** - Frontend hosting (optional)
- **GitHub** - Version control and CI/CD

### Why These Technologies?

| Technology | Why We Chose It | Alternative |
|-----------|----------------|-------------|
| **Groq** | 10x faster than OpenAI, free tier | OpenAI GPT, Anthropic Claude |
| **Cohere** | Free embeddings, 384 dimensions (small & fast) | OpenAI Embeddings (expensive) |
| **Supabase** | Free PostgreSQL + pgvector, easy setup | Pinecone (expensive), Weaviate |
| **FastAPI** | Built-in async, automatic API docs | Flask (slower), Django (overkill) |
| **Render** | Free tier, auto-deploy from GitHub | Heroku (no free tier), AWS (complex) |

---

## 🐛 Troubleshooting (Common Issues)

### Problem 1: "Module not found" Error

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem 2: "API Key Invalid" Error

**Solution:**
- Check your `.env` file exists in the `ragbackend` folder
- Make sure API keys are copied correctly (no extra spaces)
- Verify keys are active on provider websites

### Problem 3: "Port 8001 already in use"

**Solution:**
```bash
# On Windows:
netstat -ano | findstr :8001
taskkill /PID <process_id> /F

# On Mac/Linux:
lsof -ti:8001 | xargs kill -9
```

### Problem 4: PDF Upload Fails

**Possible Causes:**
- File is not a PDF
- File is corrupted
- File is encrypted/password-protected
- File is too large (>10MB)

**Solution:**
- Try a different PDF
- Ensure file is under 10MB
- Remove password protection

### Problem 5: AI Gives Wrong Answers

**Possible Causes:**
- PDF text extraction failed (scanned images)
- Question is too vague
- Relevant info not in the document

**Solution:**
- Use text-based PDFs (not scanned images)
- Ask specific questions
- Check if info is actually in the PDF

---

## 🎓 Learning Resources

### Want to Learn More?

#### For Beginners:
- [What is RAG?](https://www.youtube.com/results?search_query=rag+explained) - YouTube tutorials
- [Python Tutorial](https://www.python.org/about/gettingstarted/) - Learn Python basics
- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/) - Learn backend development

#### For Developers:
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Supabase pgvector Guide](https://supabase.com/docs/guides/ai)

#### Research Papers:
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [REALM: Retrieval-Augmented Language Model Pre-Training](https://arxiv.org/abs/2002.08909)

---

## 📞 Support & Community

### Need Help?

- **Issues**: [GitHub Issues](https://github.com/T-sashi-pavan/DOCSYAI-USING-RAG-MODEL-/issues)
- **Questions**: Open a discussion on GitHub
- **Bugs**: Report with error logs and steps to reproduce

### Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project for your own purposes.

**What this means:**
- ✅ Use for personal projects
- ✅ Use for commercial projects
- ✅ Modify the code
- ✅ Share with others
- ❌ We're not responsible for any issues
- ❌ No warranty provided

---

## 🌟 Project Status

- ✅ **Currently Deployed**: https://docsyai-using-rag-model.pages.dev
- ✅ **Production Ready**: Serving 2,600+ document chunks
- ✅ **Actively Maintained**: Regular updates and improvements
- ✅ **Mobile Responsive**: Works on all devices

### Recent Updates:
- ✨ Fixed mobile input field visibility
- ✨ Improved response formatting
- ✨ Enhanced error handling
- ✨ Added session management

---

## 🙏 Acknowledgments

Built with amazing free tools and APIs:
- **Groq** - Ultra-fast LLM inference
- **Cohere** - Free embedding API
- **Supabase** - Free PostgreSQL with pgvector
- **Render** - Free hosting platform
- **FastAPI** - Modern Python framework

---

<div align="center">

**⭐ If you find this project useful, please star the repository! ⭐**

Made with ❤️ for the open-source community

[Live Demo](https://docsyai-using-rag-model.pages.dev) | [Report Bug](https://github.com/T-sashi-pavan/DOCSYAI-USING-RAG-MODEL-/issues) | [Request Feature](https://github.com/T-sashi-pavan/DOCSYAI-USING-RAG-MODEL-/issues)

</div>
