# config.py - Central Configuration for 500MB Optimization

"""
Tune these settings based on your cloud memory and performance needs.
All settings optimized for 500MB memory by default.
"""

# ============================================================================
# MEMORY OPTIMIZATION SETTINGS (Critical for 500MB)
# ============================================================================

# PDF Processing
PDF_CHUNK_SIZE = 300  # Characters per chunk
# Smaller = less memory per chunk but more API calls for embedding
# Range: 200-700 (recommended: 300-400 for 500MB)

PDF_CHUNK_OVERLAP = 50  # Character overlap between chunks
# Keep at 50 for quality

# Embedding Batch Size (VERY IMPORTANT FOR MEMORY)
EMBEDDING_BATCH_SIZE = 2  # Texts to embed at once
# MEMORY USAGE: batch_size * 2KB ≈ 4KB at batch_size=2, 32KB at batch_size=16
# For 500MB: keep at 2-4
# For 1GB: can use 8-16
# For GPU: can use 32-64

# Streaming Buffer Size
STREAM_BUFFER_SIZE = 20  # Chunks to buffer before writing to DB
# Smaller = more DB writes but lower memory
# Range: 10-50 (recommended: 20)

# PDF Loading
PDF_LOADER_MAX_WORKERS = 1  # Parallel workers for PDF extraction
# 1 = sequential (slower but uses less memory)
# 2-4 = moderate parallelism
# NOT RECOMMENDED > 2 for 500MB
# Note: Now using streaming instead of parallel anyway

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# API Settings
API_TIMEOUT = 30  # Seconds
API_PORT = 10000
API_WORKERS = 1  # Uvicorn workers (keep at 1 for 500MB)

# LLM Settings
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model
LLM_TEMPERATURE = 0.3  # Lower = more factual
LLM_MAX_TOKENS = 800

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# RAG Search
RAG_TOP_K = 5  # Number of chunks to retrieve
RAG_THRESHOLD = 0.7  # Relevance threshold (0-1)

# ============================================================================
# GARBAGE COLLECTION (For Memory Management)
# ============================================================================

GC_INTERVAL = 10  # Force garbage collection every N pages
# Smaller = more GC overhead but freeer memory
# Recommended: 10-20

GC_AGGRESSIVE = True  # Force GC after every batch
# Keep True for 500MB deployment

# ============================================================================
# CLOUD DEPLOYMENT SETTINGS
# ============================================================================

# Memory Limits
MAX_MEMORY_MB = 500  # Your cloud instance memory
MEMORY_WARNING_THRESHOLD = 400  # Warn if memory usage exceeds this

# File Size Limits
MAX_UPLOAD_SIZE_MB = 100  # Maximum file upload size
# Recommended for 500MB: 40-50 MB
# Note: Can upload larger, but will be slower/riskier

MAX_RECOMMENDED_PDF_SIZE = 40  # For stable operation

# Request Limits
MAX_CONCURRENT_UPLOADS = 1  # Only process 1 PDF at a time
# Prevents OOM from simultaneous uploads

# Timeout for PDF Processing
PDF_PROCESSING_TIMEOUT = 300  # 5 minutes in seconds
# Increase if processing large PDFs

# ============================================================================
# CACHE SETTINGS (Optional - Uncomment if using)
# ============================================================================

# CACHE_ENABLED = False  # Disable for now
# CACHE_TTL = 3600  # 1 hour
# CACHE_MAX_EMBEDDINGS = 1000
# CACHE_MAX_ANSWERS = 500

# ============================================================================
# DATABASE SETTINGS
# ============================================================================

DB_COLLECTION_NAME = "pdf_qa_collection"
DB_BATCH_INSERT_SIZE = 100  # Insert this many at once

# Vector Search Settings
VECTOR_SEARCH_TIMEOUT = 30
VECTOR_SIMILARITY_METRIC = "cosine"

# ============================================================================
# LOGGING & MONITORING
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_PERFORMANCE_METRICS = True
LOG_MEMORY_USAGE = False  # Enable for debugging

# ============================================================================
# ADVANCED TUNING (Don't change unless you know what you're doing)
# ============================================================================

# Rate Limiting for Embeddings
EMBEDDING_RATE_LIMIT_DELAY = 1.0  # Seconds between batches
# Increase if getting "rate limited" errors

# Retry Settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds

# Health Check
HEALTH_CHECK_INTERVAL = 30  # Check every N seconds
HEALTH_CHECK_TIMEOUT = 5


# ============================================================================
# PRESETS (Use these for quick switching)
# ============================================================================

class MemoryPreset:
    """Quick configurations for different memory sizes"""
    
    @staticmethod
    def preset_500mb():
        """Optimized for 500MB cloud (current)"""
        return {
            'chunk_size': 300,
            'batch_size': 2,
            'max_workers': 1,
            'buffer_size': 20,
        }
    
    @staticmethod
    def preset_1gb():
        """For 1GB cloud instance"""
        return {
            'chunk_size': 400,
            'batch_size': 4,
            'max_workers': 2,
            'buffer_size': 30,
        }
    
    @staticmethod
    def preset_2gb():
        """For 2GB cloud instance or local machine"""
        return {
            'chunk_size': 500,
            'batch_size': 8,
            'max_workers': 4,
            'buffer_size': 50,
        }
    
    @staticmethod
    def preset_local_gpu():
        """For local machine with GPU"""
        return {
            'chunk_size': 700,
            'batch_size': 32,
            'max_workers': 8,
            'buffer_size': 100,
        }


# ============================================================================
# HOW TO USE
# ============================================================================

"""
1. In your main code, import and use:
   
   from config import (
       PDF_CHUNK_SIZE,
       EMBEDDING_BATCH_SIZE,
       RAG_TOP_K,
       MAX_MEMORY_MB,
   )
   
   # In rag_system.py:
   self.chunker = TextChunker(chunk_size=PDF_CHUNK_SIZE)
   
   # In embeddings.py:
   for batch in range(0, len(texts), EMBEDDING_BATCH_SIZE):
       ...

2. To switch presets:
   
   from config import MemoryPreset
   
   # For 1GB cloud:
   config = MemoryPreset.preset_1gb()
   PDF_CHUNK_SIZE = config['chunk_size']
   EMBEDDING_BATCH_SIZE = config['batch_size']

3. Environment-specific overrides:
   
   import os
   if os.getenv('ENVIRONMENT') == 'cloud_500mb':
       EMBEDDING_BATCH_SIZE = 2
   elif os.getenv('ENVIRONMENT') == 'cloud_1gb':
       EMBEDDING_BATCH_SIZE = 4
"""

# ============================================================================
# CLOUD PROVIDER SPECIFIC SETTINGS
# ============================================================================

class CloudPresets:
    """Settings for different cloud providers"""
    
    @staticmethod
    def render_free():
        """Render.com free tier (512MB)"""
        return {
            'max_memory': 512,
            'timeout': 120,  # Render timeout
            'workers': 1,
            'batch_size': 2,
        }
    
    @staticmethod
    def railway():
        """Railway.app ($5/month plan)"""
        return {
            'max_memory': 512,
            'timeout': 60,  # Set in railway.json
            'workers': 1,
            'batch_size': 2,
        }
    
    @staticmethod
    def flyio():
        """Fly.io with 512MB instance"""
        return {
            'max_memory': 512,
            'timeout': 120,  # Can adjust
            'workers': 1,
            'batch_size': 2,
        }
    
    @staticmethod
    def localhost():
        """Local development"""
        return {
            'max_memory': 4096,  # Usually 4GB+
            'timeout': 300,
            'workers': 4,
            'batch_size': 16,
        }


if __name__ == "__main__":
    print("Configuration file loaded successfully!")
    print(f"\nCurrent settings for 500MB:")
    print(f"  Chunk size: {PDF_CHUNK_SIZE}")
    print(f"  Batch size: {EMBEDDING_BATCH_SIZE}")
    print(f"  Buffer size: {STREAM_BUFFER_SIZE}")
    print(f"  Max workers: {PDF_LOADER_MAX_WORKERS}")
    print(f"\nTo use custom settings, modify this file and import in main.py")
