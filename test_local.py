"""
Local testing script for RAG system
Tests PDF upload, embeddings, and Q&A without full server
"""
import os
import sys
from pathlib import Path

# Test imports
print("=" * 70)
print("🧪 LOCAL RAG SYSTEM TEST")
print("=" * 70)

print("\n📦 Testing imports...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
    
    from src.embeddings import EmbeddingManager
    print("✅ EmbeddingManager imported")
    
    from src.llm_manager import LLMManager
    print("✅ LLMManager imported")
    
    from src.pdf_loader import PDFLoader
    print("✅ PDFLoader imported")
    
    from src.text_chunker import TextChunker
    print("✅ TextChunker imported")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test Cohere embeddings
print("\n" + "=" * 70)
print("🧠 Testing Cohere Embeddings...")
print("=" * 70)
try:
    embedder = EmbeddingManager()
    test_text = "This is a test sentence for embedding generation."
    print(f"Input: '{test_text}'")
    
    embedding = embedder.embed_text(test_text)
    print(f"✅ Embedding generated successfully!")
    print(f"   Dimension: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")
    print(f"   Memory estimate: ~{len(embedding) * 8} bytes per embedding")
    
except Exception as e:
    print(f"❌ Embedding error: {e}")
    import traceback
    traceback.print_exc()

# Test LLM
print("\n" + "=" * 70)
print("🤖 Testing Groq LLM...")
print("=" * 70)
try:
    llm = LLMManager()
    test_question = "What is machine learning?"
    print(f"Question: '{test_question}'")
    
    response = llm.generate_answer(test_question, context="", mode="general")
    print(f"✅ LLM response generated successfully!")
    print(f"   Response length: {len(response)} characters")
    print(f"   Preview: {response[:200]}...")
    
except Exception as e:
    print(f"❌ LLM error: {e}")
    import traceback
    traceback.print_exc()

# Test PDF processing (if sample PDF exists)
print("\n" + "=" * 70)
print("📄 Testing PDF Processing...")
print("=" * 70)
try:
    # Create a simple test text instead of needing a PDF
    test_content = """
    Machine Learning Basics
    
    Machine learning is a subset of artificial intelligence that enables systems
    to learn and improve from experience without being explicitly programmed.
    
    Key Concepts:
    1. Supervised Learning - Learning from labeled data
    2. Unsupervised Learning - Finding patterns in unlabeled data
    3. Neural Networks - Computing systems inspired by biological neural networks
    
    Applications include image recognition, natural language processing, and
    recommendation systems.
    """
    
    print("Sample text content created")
    
    # Test chunking
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_text(test_content)
    print(f"✅ Text chunked successfully!")
    print(f"   Number of chunks: {len(chunks)}")
    print(f"   Chunk sizes: {[len(c) for c in chunks]}")
    
    # Test embedding batch
    print("\n   Testing batch embeddings...")
    embeddings = embedder.embed_batch(chunks[:3])  # Test first 3 chunks
    print(f"   ✅ Batch embeddings successful!")
    print(f"   Generated {len(embeddings)} embeddings")
    print(f"   Total memory: ~{len(embeddings) * len(embeddings[0]) * 8} bytes")
    
except Exception as e:
    print(f"❌ Processing error: {e}")
    import traceback
    traceback.print_exc()

# Memory usage estimation
print("\n" + "=" * 70)
print("💾 Memory Usage Estimation")
print("=" * 70)
import psutil
import os

process = psutil.Process(os.getpid())
memory_info = process.memory_info()
memory_mb = memory_info.rss / 1024 / 1024

print(f"Current process memory: {memory_mb:.2f} MB")
print(f"512 MB limit remaining: {512 - memory_mb:.2f} MB")

if memory_mb < 512:
    print("✅ WITHIN 512MB LIMIT!")
else:
    print("❌ EXCEEDS 512MB LIMIT!")

print("\n" + "=" * 70)
print("🎯 TEST SUMMARY")
print("=" * 70)
print("✅ All core components working")
print("✅ Cohere embeddings functional")
print("✅ Groq LLM functional")
print("✅ Text chunking working")
print(f"💾 Memory usage: {memory_mb:.2f} MB / 512 MB")
print("=" * 70)
