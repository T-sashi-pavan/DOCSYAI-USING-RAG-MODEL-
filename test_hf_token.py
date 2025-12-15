"""Test HuggingFace token and embeddings."""
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing HuggingFace Setup...\n")

# Check token
hf_token = os.getenv("HUGGINGFACE_API_KEY")
print(f"1️⃣ Token found: {hf_token[:10]}...{hf_token[-5:] if hf_token else 'MISSING'}")

if not hf_token:
    print("❌ HUGGINGFACE_API_KEY not found in .env")
    print("   Get a token at: https://huggingface.co/settings/tokens")
    exit(1)

# Test InferenceClient
print("\n2️⃣ Testing InferenceClient...")
try:
    from huggingface_hub import InferenceClient
    print("✅ huggingface_hub installed")
except ImportError:
    print("❌ huggingface_hub not installed")
    print("   Run: pip install huggingface-hub")
    exit(1)

# Test embeddings
print("\n3️⃣ Testing embeddings generation...")
try:
    client = InferenceClient(token=hf_token)
    
    print("   Generating test embedding...")
    embedding = client.feature_extraction(
        text="Hello, this is a test",
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Convert to list
    if hasattr(embedding, 'tolist'):
        embedding = embedding.tolist()
    
    # Handle nested list
    if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], list):
        embedding = embedding[0]
    
    print(f"✅ Embedding generated successfully!")
    print(f"   Dimension: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nCommon fixes:")
    print("1. Regenerate token at: https://huggingface.co/settings/tokens")
    print("2. Make sure token has 'Read' access")
    print("3. Wait ~20 seconds for model to load (first request)")
    exit(1)

print("\n" + "="*60)
print("🎉 HuggingFace setup is working!")
print("="*60)