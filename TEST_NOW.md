# 🎉 SUCCESSFUL SERVER START!

## ✅ Your Server is Running!

```
✅ RAG System initialized successfully
✅ Supabase connected: pdf_qa_collection
✅ Cohere embeddings: embed-english-light-v3.0
✅ Groq LLM: llama-3.1-8b-instant
✅ Server running on: http://127.0.0.1:8001
```

---

## 🚀 TESTING IN GIT BASH (Your Current Terminal)

### Option 1: Use Shell Script (Recommended)
```bash
# Make executable
chmod +x test_api.sh

# Run all tests
./test_api.sh
```

### Option 2: Manual curl Commands

**Test 1: Health Check**
```bash
curl http://localhost:8001/
```

**Test 2: Stats**
```bash
curl http://localhost:8001/stats
```

**Test 3: Ask General Question (No PDF)**
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is machine learning?","top_k":5,"threshold":0.7}'
```

**Test 4: Upload PDF**
```bash
curl -X POST http://localhost:8001/upload \
  -F "file=@test.pdf" \
  -H "accept: application/json"
```

**Test 5: Ask Question About PDF**
```bash
# Wait 2-3 seconds after upload, then:
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the types of machine learning?","top_k":5,"threshold":0.7}'
```

---

## 🌐 TESTING IN BROWSER

### Open the Frontend
1. **In Git Bash**, run:
   ```bash
   start static/index.html
   ```
   
   Or manually open: `C:\Desktop\MACHINE LEARNING\RAG MODEL\ragbackend\static\index.html`

2. **Check Console** (Press F12):
   - Should say: `🌐 Running in: LOCAL MODE`
   - Should say: `📡 API Base: http://localhost:8001`

3. **Test Upload**:
   - Click "Upload PDF Document" in sidebar
   - Select `test.pdf`
   - Wait for "✅ PDF uploaded successfully!"

4. **Ask Questions**:
   - Type: "What is machine learning?"
   - Type: "What are the types of machine learning?"
   - Type: "Explain supervised learning"

---

## 📊 MONITOR MEMORY USAGE

### While Server is Running

**In a NEW Git Bash terminal**:
```bash
# Check memory usage
tasklist.exe //FI "IMAGENAME eq python.exe" //FO TABLE

# Or using PowerShell
powershell "Get-Process python | Select-Object ProcessName,@{Name='Memory(MB)';Expression={[math]::Round(\$_.WS / 1MB, 2)}}"
```

Expected: **100-250 MB** (well under 512 MB limit)

---

## 📋 COMPLETE TEST CHECKLIST

Run through these tests:

- [ ] **Server starts** without errors ✅ (Already done!)
- [ ] Health check returns: `{"message":"RAG PDF Q&A API is running"}`
- [ ] Stats returns: `{"total_chunks": X, "collection": "pdf_qa_collection"}`
- [ ] General question gets answer from Groq
- [ ] PDF uploads successfully
- [ ] Stats shows chunks > 0 after upload
- [ ] Question about PDF content returns relevant answer
- [ ] Browser frontend shows "LOCAL MODE"
- [ ] Memory stays under 512 MB

---

## 🎯 EXPECTED RESPONSES

### Health Check (`GET /`)
```json
{"message":"RAG PDF Q&A API is running"}
```

### Stats (`GET /stats`)
```json
{
  "total_chunks": 0,  // Will be > 0 after PDF upload
  "collection": "pdf_qa_collection"
}
```

### Ask Question (`POST /ask`)
```json
{
  "answer": "Machine learning is...",
  "sources": [...],  // Empty if no PDF, populated if PDF uploaded
  "mode": "general"  // or "pdf" if answer from document
}
```

### Upload PDF (`POST /upload`)
```json
{
  "message": "PDF uploaded and processed successfully",
  "chunks_created": 15  // Number depends on PDF size
}
```

---

## 🐛 TROUBLESHOOTING

### Server Won't Start
```bash
# Check if port 8001 is already in use
netstat -ano | grep :8001

# Kill existing process if needed
taskkill //PID <process_id> //F
```

### curl Not Working in Git Bash
```bash
# Install curl if missing
# Or use PowerShell instead:
powershell "Invoke-WebRequest -Uri http://localhost:8001/ -Method GET"
```

### psutil Module Error
```bash
# Install psutil in virtual environment
"/c/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/pip.exe" install psutil

# Then run memory test:
"/c/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/python.exe" test_memory.py
```

---

## 🚀 RESTART SERVER (If Needed)

### In Current Terminal
Press `Ctrl+C` to stop, then:
```bash
./start_server.sh
```

### Or Run in Background
```bash
./start_server.sh &
```

---

## ✅ NEXT STEPS AFTER LOCAL TESTING SUCCEEDS

1. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Tested locally - all working, ready for production"
   git push origin main
   ```

2. **Verify Render Environment Variables**:
   - Go to: https://dashboard.render.com/
   - Add same keys from `.env` file:
     - `GROQ_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`
     - `COHERE_API_KEY`

3. **Deploy**:
   - Render auto-deploys on push
   - Wait 2-3 minutes
   - Test at: https://docsyai-using-rag-model.onrender.com

4. **Test Production**:
   - Open `static/index.html` in browser
   - Frontend auto-switches to production URL
   - Test PDF upload and Q&A

---

## 📁 Quick Reference

### Files for Testing
- `test_api.sh` - Automated API tests (Git Bash)
- `test_api.bat` - Automated API tests (CMD/PowerShell)
- `start_server.sh` - Start server (Git Bash)
- `start_server.bat` - Start server (CMD/PowerShell)
- `test.pdf` - Sample PDF for testing
- `static/index.html` - Frontend (auto-detects local/production)

### API Endpoints
- `GET /` - Health check
- `GET /stats` - Collection statistics
- `POST /upload` - Upload PDF (multipart/form-data)
- `POST /ask` - Ask question (JSON body)

### Local URLs
- Backend: http://localhost:8001
- Frontend: file:///C:/Desktop/MACHINE%20LEARNING/RAG%20MODEL/ragbackend/static/index.html
- API Docs: http://localhost:8001/docs (FastAPI Swagger UI)

---

**Your server is running! Test it now with the commands above.** 🚀
