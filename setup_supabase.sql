-- ============================================================================
-- Supabase Database Setup for RAG Backend
-- ============================================================================
-- This script sets up the required table and vector extension for the RAG system
-- Run this in your Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql
-- ============================================================================

-- 1. Enable the pgvector extension (required for vector similarity search)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create the pdf_qa_collection table
CREATE TABLE IF NOT EXISTS pdf_qa_collection (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(384),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Create an index for fast vector similarity search
-- Using ivfflat index with cosine distance for efficient similarity search
CREATE INDEX IF NOT EXISTS pdf_qa_collection_embedding_idx 
ON pdf_qa_collection 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 4. Create an index on created_at for faster sorting
CREATE INDEX IF NOT EXISTS pdf_qa_collection_created_at_idx 
ON pdf_qa_collection (created_at DESC);

-- 5. Create the match_documents function for vector similarity search
CREATE OR REPLACE FUNCTION match_documents (
    query_embedding VECTOR(384),
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id TEXT,
    text TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pdf_qa_collection.id,
        pdf_qa_collection.text,
        pdf_qa_collection.metadata,
        1 - (pdf_qa_collection.embedding <=> query_embedding) AS similarity
    FROM pdf_qa_collection
    ORDER BY pdf_qa_collection.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 6. Verify the table was created successfully
SELECT 
    table_name, 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_name = 'pdf_qa_collection'
ORDER BY ordinal_position;

-- 7. Verify the function was created
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_name = 'match_documents';

-- ============================================================================
-- Setup Complete!
-- ============================================================================
-- Your database is now ready with:
-- ✅ pgvector extension enabled
-- ✅ pdf_qa_collection table created
-- ✅ Vector similarity indexes created
-- ✅ match_documents function for searching
--
-- You can now upload PDFs and ask questions through the API!
-- ============================================================================
