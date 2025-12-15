-- ============================================================================
-- QUICK FIX: Add match_documents function to enable /ask endpoint
-- ============================================================================
-- Run this in Supabase SQL Editor to fix the search functionality
-- ============================================================================

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

-- Verify the function was created
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_name = 'match_documents';

-- ============================================================================
-- Done! You can now use the /ask endpoint to query your PDFs.
-- ============================================================================
