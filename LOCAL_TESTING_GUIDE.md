# RAG System - Local Testing Guide

## ✅ Memory Test Results
- **Current usage**: 71.43 MB / 512 MB (14% utilization)
- **Safety margin**: 440.57 MB (86%)
- **Status**: ✅ WELL WITHIN 512MB LIMIT

## 🔑 Required Setup

### 1. Get FREE Cohere API Key
1. Go to: https://dashboard.cohere.com/api-keys
2. Sign up for free account
3. Copy your API key
4. Add to `.env` file:
   ```
   COHERE_API_KEY=your_actual_key_here
   ```

### 2. Verify Supabase Credentials
1. Go to: https://app.supabase.com/
2. Open your project: hjzalxzfgtbrokhdxhkt
3. Go to Settings → API
4. Copy the `anon` `public` key
5. Update `.env` file:
   ```
   SUPABASE_ANON_KEY=your_actual_anon_key_here
   ```

## 🚀 Local Testing Steps

### Step 1: Start Backend Server
```bash
cd "C:/Desktop/MACHINE LEARNING/RAG MODEL/ragbackend"
"C:/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### Step 2: Open Frontend
1. Open `static/index.html` in your browser
2. Check browser console - should say: "🌐 Running in: LOCAL MODE"
3. API Base should be: http://localhost:8001

### Step 3: Test with cURL

#### Test 1: Health Check
```bash
curl http://localhost:8001/
```
Expected: `{"message":"RAG PDF Q&A API is running"}`

#### Test 2: Stats Check
```bash
curl http://localhost:8001/stats
```
Expected: JSON with `total_chunks` and `collection`

#### Test 3: Upload PDF
```bash
# Create a test PDF first, or use existing one
curl -X POST http://localhost:8001/upload \
  -F "file=@path/to/your/test.pdf" \
  -H "accept: application/json"
```
Expected: `{"message":"PDF uploaded successfully"}`

#### Test 4: Ask Question
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\",\"top_k\":5,\"threshold\":0.7}"
```
Expected: JSON with `answer`, `sources`, `mode`

### Step 4: Monitor Memory Usage
```powershell
# While server is running, check memory in another terminal
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
```

## 🧪 Automated Test Script

Run the comprehensive test:
```bash
"C:/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/python.exe" test_memory.py
```

## 📊 Expected Performance

### Memory Usage
- Baseline: ~18 MB
- With all imports: ~68 MB
- After PDF processing: ~150-250 MB (depends on PDF size)
- **Maximum**: Should stay under 512 MB

### Response Times
- PDF upload: 2-5 seconds (small PDFs)
- Embedding generation: 1-3 seconds per batch
- Question answering: 2-4 seconds

## 🐛 Troubleshooting

### Issue: "Invalid API key" for Cohere
**Solution**: Replace `TRIAL_KEY` with real key from https://dashboard.cohere.com/api-keys

### Issue: "Invalid API key" for Supabase
**Solution**: 
1. Go to https://app.supabase.com/project/hjzalxzfgtbrokhdxhkt/settings/api
2. Copy the `anon` `public` key (starts with `eyJ...`)
3. Update `.env` file

### Issue: Port 8001 already in use
**Solution**: 
```bash
# Find and kill process
netstat -ano | findstr :8001
taskkill /PID <process_id> /F
```

### Issue: Memory exceeds 512MB
**Solution**: Check `config.py` settings:
- Reduce `EMBEDDING_BATCH_SIZE` (default: 2)
- Reduce `PDF_CHUNK_SIZE` (default: 300)

## ✅ Deployment Checklist

Before deploying to Render:
- [ ] Memory test passes (< 512 MB)
- [ ] PDF upload works locally
- [ ] Question answering works locally
- [ ] Valid Cohere API key set
- [ ] Valid Supabase credentials set
- [ ] All curl tests pass
- [ ] Browser frontend works in local mode

After local testing succeeds:
- [ ] Commit changes to GitHub
- [ ] Add API keys to Render environment variables
- [ ] Deploy to Render
- [ ] Test with production URL
- [ ] Frontend auto-switches to production mode

## 🎯 Current Status
- ✅ Frontend: Auto-detects local vs production
- ✅ Backend: Running on port 8001
- ✅ Memory: 71.43 MB (14% of 512 MB limit)
- ⚠️ API Keys: Need valid Cohere key
- ⚠️ Supabase: Need valid credentials
