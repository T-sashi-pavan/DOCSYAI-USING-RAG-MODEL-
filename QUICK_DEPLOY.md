# Quick Deployment Guide - Render + Cloudflare

## 🚀 Deploy in 10 Minutes

### Step 1: Deploy Backend to Render (5 min)

1. Push code to GitHub:
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

2. Go to [render.com](https://render.com) → **New +** → **Web Service**

3. Connect GitHub and select your repository

4. Configure:
```
Name: rag-chatbot-backend
Environment: Python 3
Build Command: pip install --no-cache-dir -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

5. Add Environment Variables:
```
GROQ_API_KEY = your_key
HUGGINGFACE_TOKEN = your_token
SUPABASE_URL = your_url
SUPABASE_ANON_KEY = your_key
PYTHON_VERSION = 3.11.0
```

6. Click **Create Web Service**

7. **Copy your Render URL**: `https://rag-chatbot-backend.onrender.com`

---

### Step 2: Deploy Frontend to Cloudflare (5 min)

1. Update `static/index.html` line 1389:
```javascript
const API_BASE = 'https://rag-chatbot-backend.onrender.com';
```

2. Commit and push:
```bash
git add static/index.html
git commit -m "Update API for production"
git push origin main
```

3. Go to [pages.cloudflare.com](https://pages.cloudflare.com) → **Create project**

4. Connect GitHub and select repository

5. Configure:
```
Build command: (empty)
Build output directory: /static
```

6. Click **Save and Deploy**

---

### Step 3: Test (1 min)

1. Open your Cloudflare Pages URL
2. Upload a PDF
3. Ask a question
4. ✅ Done!

---

## ⚠️ Important Notes

- **Render sleeps after 15 min**: First request takes 30-50s to wake up
- **Free tier**: 750 hours/month (perfect for testing)
- **Auto-deploy**: Every git push triggers new deployment
- **HTTPS**: Both Render and Cloudflare provide free SSL

---

## 🔧 Troubleshooting

**Slow first response?**
- Normal! Render wakes from sleep (30-50s)

**CORS error?**
- Update `main.py` with your Cloudflare Pages URL

**PDF upload fails?**
- Wait for backend to wake up
- Try smaller PDF (<10MB)

---

## 📊 What You Get

✅ Free hosting for frontend AND backend  
✅ Auto-deploy on git push  
✅ Free HTTPS/SSL  
✅ Global CDN (Cloudflare)  
✅ No credit card required  

**Total cost: $0/month**

---

## 🔄 Quick Commands

```bash
# Update backend
git add .
git commit -m "Update"
git push origin main
# Render auto-deploys in 2-3 min

# Check Render logs
# Go to render.com → Your service → Logs

# Check Cloudflare deployment
# Go to pages.cloudflare.com → Your project → Deployments
```

That's it! Your RAG chatbot is live! 🎉
