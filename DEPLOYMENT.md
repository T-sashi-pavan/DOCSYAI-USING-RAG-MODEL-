# RAG Chatbot - Production Deployment Guide

Complete guide for deploying your RAG chatbot using **100% free cloud services** with **fast deployment**.

## 🌐 Architecture Overview

- **Frontend**: Cloudflare Pages (FREE)
- **Backend**: Render.com (FREE tier - 750 hours/month)
- **Vector Database**: Supabase (FREE tier - 500MB)
- **LLM**: Groq API (FREE with rate limits)
- **Embeddings**: HuggingFace Inference API (FREE)

> **Note**: This setup uses Render for fast deployment. You can migrate to Google Cloud e2-micro later if needed.

---

## 📋 Prerequisites

Before starting, ensure you have:

1. ✅ GitHub account (for code repository)
2. ✅ Render.com account (for backend hosting)
3. ✅ Cloudflare account (for Pages deployment)
4. ✅ Supabase account (already configured)
5. ✅ Groq API key (already have)
6. ✅ HuggingFace token (already have)

---

## 🚀 Part 1: Backend Deployment (Render.com)

### Step 1: Push Your Code to GitHub

Your code is already on GitHub. Ensure it's up to date:

```bash
cd "c:\Desktop\MACHINE LEARNING\RAG MODEL\ragbackend"
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account & Deploy

1. Go to [Render.com](https://render.com/) and sign up (free)
2. Click **New +** → **Web Service**
3. Connect your GitHub account
4. Select your repository (`ragbackend`)
5. Configure the service:

**Basic Settings:**
```
Name: rag-chatbot-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: (leave empty)
Environment: Python 3
```

**Build & Deploy:**
```
Build Command: pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Plan:**
```
Instance Type: Free (750 hours/month)
```

6. Click **Advanced** and add environment variables:

```
GROQ_API_KEY = your_groq_api_key
HUGGINGFACE_TOKEN = your_huggingface_token
SUPABASE_URL = your_supabase_url
SUPABASE_ANON_KEY = your_supabase_anon_key
PYTHON_VERSION = 3.11.0
```

7. Click **Create Web Service**

### Step 3: Wait for Deployment

Render will:
- ✅ Clone your repository
- ✅ Install dependencies from requirements.txt
- ✅ Start your FastAPI application
- ✅ Provide you with a URL like: `https://rag-chatbot-backend.onrender.com`

**Deployment takes 3-5 minutes** ⏱️

### Step 4: Verify Backend is Running

Once deployment completes, test your backend:

```bash
# Test API endpoint (replace with your Render URL)
curl https://rag-chatbot-backend.onrender.com/api
```

Expected response:
```json
{"message":"PDF Q&A API is running","endpoints":["/upload","/ask","/stats"]}
```

**Your backend URL is:** `https://rag-chatbot-backend.onrender.com`

> **Important**: Free tier sleeps after 15 minutes of inactivity. First request may take 30-50 seconds to wake up.

---

## 🎨 Part 2: Frontend Deployment (Cloudflare Pages)

### Step 1: Update API Endpoint

1. **On your local machine**, open [static/index.html](static/index.html)

2. **Find line ~1389** and update API_BASE:

```javascript
// Change from:
const API_BASE = 'http://localhost:10000';

// To (replace with your actual Render URL):
const API_BASE = 'https://rag-chatbot-backend.onrender.com';
```

3. **Save the file**

### Step 2: Commit Changes

```bash
git add static/index.html
git commit -m "Update API_BASE for production"
git push origin main
```

### Step 3: Deploy to Cloudflare Pages

**Option A: Direct GitHub Connection (Recommended)**

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Click **Create a project**
3. Click **Connect to Git**
4. Select your GitHub repository
5. Configure build settings:

```
Project name: rag-chatbot
Production branch: main
Build command: (leave empty)
Build output directory: /static
```

6. Click **Save and Deploy**
7. Wait 1-2 minutes for deployment

**Option B: Direct Upload**

1. Create a local build folder:
```bash
mkdir cloudflare-build
cp static/index.html cloudflare-build/
```

2. Go to Cloudflare Pages → **Create a project** → **Upload assets**
3. Drag and drop the `cloudflare-build` folder
4. Click **Deploy**

### Step 4: Get Your Frontend URL

After deployment completes, Cloudflare will provide a URL like:
```
https://rag-chatbot.pages.dev
```

---

## 🔧 Part 3: Final Configuration

### Update CORS in Backend (on Render)

1. Go to your Render dashboard
2. Select your web service (`rag-chatbot-backend`)
3. Go to **Environment** tab
4. Add a new environment variable:

```
ALLOWED_ORIGINS = https://rag-chatbot.pages.dev
```

5. Or manually edit `main.py` in your repository:

Find the CORS middleware section (around line 18-24):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Update to:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rag-chatbot.pages.dev",  # Your Cloudflare Pages URL
        "http://localhost:10000"  # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

6. Commit and push (Render will auto-deploy):
```bash
git add main.py
git commit -m "Update CORS for production"
git push origin main
```

---

## ✅ Part 4: Testing Your Deployment

### Test Backend API

```bash
# From your local machine (replace with your Render URL)
curl https://rag-chatbot-backend.onrender.com/api

# Expected response:
# {"message":"PDF Q&A API is running","endpoints":["/upload","/ask","/stats"]}
```

> **Note**: If backend was sleeping, first request may take 30-50 seconds

### Test Frontend

1. Open `https://rag-chatbot.pages.dev` in your browser
2. Click **Upload PDF** and select a PDF file
3. Wait for processing confirmation (may take 30-50s if backend was asleep)
4. Type a question and click Send
5. Verify bot responds with formatted answer

### Test Full Flow

1. **Upload a test PDF** (e.g., research paper, documentation)
2. **Ask questions:**
   - "What is this document about?"
   - "Summarize the main points"
   - "What are the key findings?"
3. **Verify responses** include proper formatting and source attribution

---

## 📊 Part 5: Monitoring & Maintenance

### Check Backend Logs (Render)

1. Go to Render Dashboard
2. Select your web service
3. Click **Logs** tab
4. View real-time logs

### Check Deployment Status

**Render:**
- Dashboard shows deployment status
- Green = Running
- Yellow = Building
- Red = Failed

**Cloudflare Pages:**
- Go to Workers & Pages → Your project
- View deployment history
- Each commit triggers a new deployment

### Update Backend Code

```bash
# Make changes locally
git add .
git commit -m "Update backend"
git push origin main

# Render automatically deploys in 2-3 minutes
```

### Update Frontend Code

```bash
# Make changes to static/index.html
git add static/index.html
git commit -m "Update frontend"
git push origin main

# Cloudflare automatically deploys in 1-2 minutes
```

### Monitor Resource Usage

**Render Free Tier Limits:**
- ✅ 750 hours/month (automatically resets)
- ✅ 512MB RAM
- ✅ Sleeps after 15 min inactivity
- ✅ Wakes on first request (~30-50s)

**Supabase:**
- Check dashboard for storage usage
- Free tier: 500MB database storage
- Your 821 chunks use ~10-20MB

---

## 🚨 Troubleshooting

### Backend Not Responding (Render)

**Issue**: 504 Gateway Timeout or slow response

**Solution**:
- First request after sleep takes 30-50 seconds (normal)
- Check Render logs for errors
- Verify environment variables are set correctly
- Restart service from Render dashboard

### Render Build Failed

**Common issues:**
1. **Missing dependencies**: Check requirements.txt
2. **Python version**: Ensure `PYTHON_VERSION=3.11` is set
3. **Build command**: Should be `pip install --no-cache-dir -r requirements.txt`
4. **Start command**: Should be `uvicorn main:app --host 0.0.0.0 --port $PORT`

### CORS Errors in Frontend

1. Check browser console for exact error
2. Verify Cloudflare Pages URL in `main.py` CORS settings
3. Push changes to trigger Render auto-deploy
4. Wait 2-3 minutes for deployment

### PDF Upload Fails

**Issue**: Upload times out or fails

**Possible causes:**
1. **Backend sleeping**: Wait 30-50s for wake-up, try again
2. **File too large**: Free tier has memory limits, try smaller PDFs (<10MB)
3. **Check Render logs**: May show specific error

**Solution**:
```bash
# Reduce chunk size in config.py if memory issues
CHUNK_SIZE = 200  # Reduce from 300
BATCH_SIZE = 1    # Reduce from 2
```

### Supabase Connection Issues

1. Go to Render Dashboard → Environment variables
2. Verify:
   - `SUPABASE_URL` is correct
   - `SUPABASE_ANON_KEY` is the anon/public key (not service key)
3. Test connection from Render Shell (if available)

### Cloudflare Pages Build Failed

1. Check build logs in Cloudflare dashboard
2. Verify build settings:
   - Build output directory: `/static`
   - Build command: (empty)
3. Ensure `static/index.html` exists in repository

---

## 💰 Cost Breakdown

| Service | Tier | Monthly Cost | Limits |
|---------|------|--------------|--------|
| Render.com | Free | $0 | 750 hours, sleeps after 15min |
| Cloudflare Pages | Free | $0 | Unlimited bandwidth |
| Supabase | Free | $0 | 500MB storage, 2GB transfer |
| Groq API | Free | $0 | Rate-limited |
| HuggingFace | Free | $0 | Serverless inference |
| **TOTAL** | | **$0/month** | |

**⚠️ Important Notes:**
- **Render Free Tier**: Sleeps after 15 minutes of inactivity. First request takes 30-50s to wake up.
- **750 hours/month**: Enough for continuous uptime if you upgrade to paid ($7/month for always-on)
- **Cloudflare Pages**: Truly unlimited on free tier
- **Supabase**: 500MB is plenty for most use cases

---

## 🔄 Migrating to Google Cloud Later

When ready to move to Google Cloud e2-micro for always-on backend:

### Why Migrate?
- ✅ Always-on (no cold starts)
- ✅ More control over server
- ✅ Same 1GB RAM as Render
- ✅ Still free (Google Cloud always-free tier)

### Migration Steps

1. **Create Google Cloud e2-micro VM** (see `deployment/deploy_gcp.sh`)
2. **Get VM External IP**
3. **Update frontend API_BASE**:
   ```javascript
   const API_BASE = 'http://YOUR_VM_IP';
   ```
4. **Push to GitHub** (triggers Cloudflare auto-deploy)
5. **Pause Render service** (or delete to save hours)

> Full Google Cloud deployment guide available in `deployment/` folder

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Supabase Documentation](https://supabase.com/docs)
- [Groq API Docs](https://console.groq.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 Success Checklist

- [ ] GitHub repository pushed and up to date
- [ ] Render web service created and deployed
- [ ] Backend API accessible via Render URL
- [ ] Frontend `index.html` updated with Render URL
- [ ] Cloudflare Pages deployed successfully
- [ ] CORS configured for Cloudflare domain
- [ ] PDF upload working from frontend
- [ ] Questions getting answered correctly
- [ ] No CORS errors in browser console
- [ ] Supabase database receiving embeddings

**Congratulations! Your RAG chatbot is now live with fast, free hosting! 🎊**

**Total deployment time: ~10-15 minutes**

---

## 🔄 Quick Reference Commands

```bash
# Update Backend
git add .
git commit -m "Update backend"
git push origin main
# Render auto-deploys in 2-3 minutes

# Update Frontend
git add static/index.html
git commit -m "Update frontend"
git push origin main
# Cloudflare auto-deploys in 1-2 minutes

# Check Render Logs
# Go to: render.com → Your Service → Logs

# Test Backend API
curl https://your-backend.onrender.com/api

# Test Frontend
# Open: https://your-project.pages.dev
```

Need help? Check the **Troubleshooting** section above or:
- Render logs for backend errors
- Browser console for frontend errors
- Supabase dashboard for database issues
