# 🔧 Supabase Database Setup Guide

## Problem
You're getting this error:
```
"Could not find the table 'public.pdf_qa_collection' in the schema cache"
```

This means the database table hasn't been created in Supabase yet.

## Solution: Create the Table in Supabase

### Step 1: Open Supabase SQL Editor

1. Go to https://supabase.com/dashboard
2. Select your project
3. Click on **SQL Editor** in the left sidebar (looks like `</>`)

### Step 2: Run the Setup SQL

1. Click **"+ New Query"**
2. Copy the entire contents of `setup_supabase.sql` file
3. Paste it into the SQL editor
4. Click **"Run"** or press `Ctrl+Enter`

### Step 3: Verify Setup

You should see a success message and a table showing the columns:
- `id` (TEXT)
- `text` (TEXT)
- `embedding` (VECTOR)
- `metadata` (JSONB)
- `created_at` (TIMESTAMP)

### Step 4: Test Your API

After creating the table:

1. **Restart your server** if it's still running (Ctrl+C, then run again)
   ```bash
   venv/Scripts/python.exe main.py
   ```

2. **Upload a PDF** - it should now work!
   ```bash
   curl -X POST "http://localhost:10000/upload" -F "file=@your-file.pdf"
   ```

3. **Check stats** - should now show document count
   ```bash
   curl http://localhost:10000/stats
   ```

## What the SQL Does

1. ✅ Enables `pgvector` extension (for vector similarity search)
2. ✅ Creates `pdf_qa_collection` table with proper schema
3. ✅ Creates indexes for fast similarity search
4. ✅ Sets up proper data types for embeddings (384 dimensions)

## Quick Alternative: Use Supabase Table Editor

If you prefer a GUI:

1. Go to **Table Editor** in Supabase dashboard
2. Click **"New Table"**
3. Name it: `pdf_qa_collection`
4. Add columns manually:
   - `id` - type: text (primary key)
   - `text` - type: text
   - `embedding` - type: vector(384)
   - `metadata` - type: jsonb
   - `created_at` - type: timestamp with time zone

**Note**: Using the SQL script is recommended as it also creates the necessary indexes.

## Troubleshooting

### Error: "extension vector does not exist"
- The pgvector extension isn't enabled
- Re-run step 1 of the SQL: `CREATE EXTENSION IF NOT EXISTS vector;`

### Error: "permission denied"
- Make sure you're using the SQL Editor as the project owner
- Check your Supabase project role permissions

### Table created but still getting errors?
- Restart your FastAPI server
- Check your SUPABASE_URL and SUPABASE_ANON_KEY are correct in .env
- Verify the table name is exactly `pdf_qa_collection` (case-sensitive)
