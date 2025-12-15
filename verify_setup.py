"""Verify all components are working."""

print("🔍 Verifying Setup...\n")

# Test 1: Check .env file
print("1️⃣ Checking .env file...")
import os
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if groq_key and groq_key.startswith("gsk_"):
    print("✅ Groq API key found")
else:
    print("❌ Groq API key not found or invalid")
    print("   Make sure your .env file has: GROQ_API_KEY=gsk_...")
    exit(1)

# Test 2: Check imports
print("\n2️⃣ Checking imports...")
try:
    from src.pdf_loader import PDFLoader
    from src.text_chunker import TextChunker
    from src.embeddings import EmbeddingManager
    from src.vector_store import VectorStore
    from src.llm_manager import LLMManager
    from src.rag_system import RAGSystem
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test 3: Test Groq connection
print("\n3️⃣ Testing Groq connection...")
try:
    from groq import Groq
    client = Groq(
        api_key=groq_key,
        timeout=30.0
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hi"}],
        max_tokens=10
    )
    print(f"✅ Groq is working! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Groq error: {e}")
    exit(1)

# Test 4: Check embeddings
print("\n4️⃣ Testing embeddings...")
try:
    embedder = EmbeddingManager()
    embedding = embedder.embed_text("test")
    print(f"✅ Embeddings working (dimension: {len(embedding)})")
except Exception as e:
    print(f"❌ Embedding error: {e}")
    exit(1)

print("\n" + "="*60)
print("🎉 All systems operational!")
print("="*60)
print("\nYou're ready to use the PDF Q&A system!")
print("Next step: Put a PDF in data/sample.pdf and run test_basic.py")