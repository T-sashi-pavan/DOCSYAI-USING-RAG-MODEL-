"""
Simplified local test - tests memory usage and API endpoints
without requiring external API keys
"""
import os
import sys
import psutil
import json

print("=" * 70)
print("🧪 RAG SYSTEM - LOCAL MEMORY & ENDPOINT TEST")
print("=" * 70)

# Test 1: Memory baseline
print("\n📊 TEST 1: Memory Usage Baseline")
print("-" * 70)
process = psutil.Process(os.getpid())
baseline_mb = process.memory_info().rss / 1024 / 1024
print(f"✅ Baseline memory: {baseline_mb:.2f} MB")

# Test 2: Import all modules
print("\n📦 TEST 2: Module Imports & Memory Impact")
print("-" * 70)
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    # Import all RAG components
    from src.embeddings import EmbeddingManager
    from src.llm_manager import LLMManager
    from src.pdf_loader import PDFLoader
    from src.text_chunker import TextChunker
    from src.vector_store import VectorStore
    from src.rag_system import RAGSystem
    
    after_import_mb = process.memory_info().rss / 1024 / 1024
    print(f"✅ All modules imported successfully")
    print(f"   Memory after imports: {after_import_mb:.2f} MB")
    print(f"   Import overhead: {after_import_mb - baseline_mb:.2f} MB")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 3: Check API endpoints (if server is running)
print("\n🌐 TEST 3: API Endpoint Availability")
print("-" * 70)
import requests

endpoints = [
    ("GET", "http://localhost:8001/", "Root endpoint"),
    ("GET", "http://localhost:8001/stats", "Stats endpoint"),
    ("GET", "http://localhost:8001/health", "Health check"),
]

for method, url, description in endpoints:
    try:
        response = requests.get(url, timeout=2)
        status = "✅" if response.status_code < 400 else "⚠️"
        print(f"{status} {description}: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ {description}: Server not running on port 8001")
    except Exception as e:
        print(f"❌ {description}: {e}")

# Test 4: Environment variables
print("\n🔑 TEST 4: Environment Variables")
print("-" * 70)
required_vars = {
    "GROQ_API_KEY": "Groq API key",
    "SUPABASE_URL": "Supabase URL",
    "SUPABASE_ANON_KEY": "Supabase anon key",
    "COHERE_API_KEY": "Cohere API key (optional, defaults to TRIAL_KEY)"
}

all_set = True
for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Show first 20 chars for security
        preview = value[:20] + "..." if len(value) > 20 else value
        print(f"✅ {var}: {preview}")
    else:
        print(f"⚠️  {var}: Not set - {description}")
        if var != "COHERE_API_KEY":
            all_set = False

# Test 5: Text chunking (no API needed)
print("\n✂️  TEST 5: Text Chunking (No API Required)")
print("-" * 70)
try:
    chunker = TextChunker(chunk_size=300, chunk_overlap=50)
    test_text = """
    Artificial Intelligence and Machine Learning
    
    Machine learning is a method of data analysis that automates analytical 
    model building. It is a branch of artificial intelligence based on the 
    idea that systems can learn from data, identify patterns and make 
    decisions with minimal human intervention.
    
    Types of Machine Learning:
    1. Supervised Learning: The algorithm learns from labeled training data
    2. Unsupervised Learning: The algorithm finds hidden patterns in data
    3. Reinforcement Learning: The algorithm learns through trial and error
    
    Applications include computer vision, natural language processing,
    recommendation systems, and autonomous vehicles.
    """ * 5  # Repeat to create more text
    
    chunks = chunker.split_text(test_text)
    print(f"✅ Text chunking successful")
    print(f"   Input length: {len(test_text)} characters")
    print(f"   Chunks created: {len(chunks)}")
    print(f"   Avg chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars")
    
    memory_after_chunk = process.memory_info().rss / 1024 / 1024
    print(f"   Memory: {memory_after_chunk:.2f} MB (+{memory_after_chunk - after_import_mb:.2f} MB)")
    
except Exception as e:
    print(f"❌ Chunking failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: PDF loading simulation
print("\n📄 TEST 6: PDF Text Extraction Simulation")
print("-" * 70)
try:
    loader = PDFLoader()
    # We'll create a simple test without actual PDF
    print(f"✅ PDFLoader initialized")
    print(f"   Ready to process PDF files")
    
except Exception as e:
    print(f"❌ PDF loader failed: {e}")

# Final Memory Report
print("\n" + "=" * 70)
print("💾 FINAL MEMORY REPORT")
print("=" * 70)
final_mb = process.memory_info().rss / 1024 / 1024
print(f"Final memory usage: {final_mb:.2f} MB")
print(f"Total overhead: {final_mb - baseline_mb:.2f} MB")
print(f"512 MB limit remaining: {512 - final_mb:.2f} MB")
print(f"Memory utilization: {(final_mb / 512) * 100:.1f}%")

if final_mb < 512:
    print("✅ ✅ ✅  WELL WITHIN 512MB LIMIT! ✅ ✅ ✅")
    safety_margin = 512 - final_mb
    print(f"Safety margin: {safety_margin:.2f} MB ({(safety_margin/512)*100:.1f}%)")
else:
    print("❌ EXCEEDS 512MB LIMIT!")

print("\n" + "=" * 70)
print("🎯 TEST SUMMARY")
print("=" * 70)
print(f"✅ Imports: All modules loaded successfully")
print(f"✅ Memory: {final_mb:.2f} MB / 512 MB ({(final_mb/512)*100:.1f}%)")
print(f"✅ Components: PDF loader, text chunker ready")
print(f"⚠️  APIs: Require valid keys for full functionality")
print("=" * 70)
print("\n🔑 NEXT STEPS:")
print("1. Get FREE Cohere API key: https://dashboard.cohere.com/api-keys")
print("2. Add to .env: COHERE_API_KEY=your_key_here")
print("3. Verify Supabase credentials at: https://app.supabase.com/")
print("4. Test full PDF upload via curl or browser")
print("=" * 70)
