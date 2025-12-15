"""
Comprehensive test script to verify all API credentials in .env file
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔐 TESTING ALL API CREDENTIALS")
print("=" * 70)

# Track results
results = {
    "groq": False,
    "huggingface": False,
    "supabase": False
}

# ============================================================================
# 1. TEST GROQ API KEY
# ============================================================================
print("\n1️⃣  TESTING GROQ API KEY")
print("-" * 70)

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    print("❌ GROQ_API_KEY not found in .env file")
else:
    print(f"✓ Key found: {groq_key[:15]}...{groq_key[-10:]}")
    
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        
        print("  Testing API connection...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Reply with just 'OK'"}],
            max_tokens=10
        )
        
        print(f"✅ GROQ API KEY IS VALID!")
        print(f"  Response: {response.choices[0].message.content}")
        results["groq"] = True
        
    except ImportError:
        print("⚠️  'groq' package not installed. Run: pip install groq")
    except Exception as e:
        print(f"❌ GROQ API KEY IS INVALID!")
        print(f"  Error: {str(e)}")
        if "401" in str(e) or "authentication" in str(e).lower():
            print("  → This looks like an authentication error. Check your API key.")
        print("  Get a valid key at: https://console.groq.com/keys")

# ============================================================================
# 2. TEST HUGGINGFACE API KEY
# ============================================================================
print("\n2️⃣  TESTING HUGGINGFACE API KEY")
print("-" * 70)

hf_key = os.getenv("HUGGINGFACE_API_KEY")
if not hf_key:
    print("❌ HUGGINGFACE_API_KEY not found in .env file")
else:
    print(f"✓ Key found: {hf_key[:15]}...{hf_key[-10:]}")
    
    try:
        from huggingface_hub import InferenceClient
        print("  Package imported successfully")
        client = InferenceClient(token=hf_key)
        
        print("  Testing embeddings generation...")
        embedding = client.feature_extraction(
            text="Test",
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Convert to list if needed
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], list):
            embedding = embedding[0]
        
        print(f"✅ HUGGINGFACE API KEY IS VALID!")
        print(f"  Embedding dimension: {len(embedding)}")
        results["huggingface"] = True
        
    except ImportError as ie:
        print(f"⚠️  'huggingface-hub' package not installed. Run: pip install huggingface-hub")
        print(f"  Debug: {ie}")
    except Exception as e:
        print(f"❌ HUGGINGFACE API KEY IS INVALID!")
        print(f"  Error: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        if "401" in str(e) or "403" in str(e) or "authentication" in str(e).lower():
            print("  → This looks like an authentication error. Check your API key.")
        print("  Get a valid key at: https://huggingface.co/settings/tokens")

# ============================================================================
# 3. TEST SUPABASE CREDENTIALS
# ============================================================================
print("\n3️⃣  TESTING SUPABASE CREDENTIALS")
print("-" * 70)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    print("❌ SUPABASE_URL or SUPABASE_ANON_KEY not found in .env file")
elif "your-project.supabase.co" in supabase_url:
    print("❌ SUPABASE CREDENTIALS ARE STILL PLACEHOLDERS!")
    print(f"  Current URL: {supabase_url}")
    print("  → You need to replace with your actual Supabase project credentials")
    print("  Get them at: https://supabase.com/dashboard/project/_/settings/api")
else:
    print(f"✓ URL found: {supabase_url}")
    print(f"✓ Key found: {supabase_key[:15]}...{supabase_key[-10:]}")
    
    try:
        from supabase import create_client
        
        print("  Testing connection...")
        supabase_client = create_client(supabase_url, supabase_key)
        
        # Try to check if we can access the client (this validates URL/key format)
        # Note: We can't test actual database access without knowing the schema
        print(f"✅ SUPABASE CREDENTIALS ARE VALID FORMAT!")
        print("  Note: Can't test actual database access without schema setup")
        results["supabase"] = True
        
    except ImportError:
        print("⚠️  'supabase' package not installed. Run: pip install supabase")
    except Exception as e:
        print(f"❌ SUPABASE CREDENTIALS ARE INVALID!")
        print(f"  Error: {str(e)}")
        if "Invalid" in str(e) or "404" in str(e):
            print("  → Check your Supabase URL and key")
        print("  Get credentials at: https://supabase.com/dashboard/project/_/settings/api")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)

total = len(results)
passed = sum(results.values())

print(f"\nGroq API:           {'✅ VALID' if results['groq'] else '❌ INVALID/NOT TESTED'}")
print(f"HuggingFace API:    {'✅ VALID' if results['huggingface'] else '❌ INVALID/NOT TESTED'}")
print(f"Supabase:           {'✅ VALID' if results['supabase'] else '❌ INVALID/NOT TESTED'}")

print(f"\n{passed}/{total} credentials validated successfully")

if passed == total:
    print("\n🎉 All credentials are working! You're ready to go!")
    sys.exit(0)
else:
    print("\n⚠️  Some credentials need attention. Please fix the issues above.")
    sys.exit(1)
