from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test all available production models
models_to_test = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile", 
    "gemma2-9b-it"
]

print("🔍 Testing Groq Models...\n")

for model in models_to_test:
    try:
        print(f"Testing {model}...", end=" ")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hi"}],
            max_tokens=10
        )
        print(f"✅ WORKS! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")

print("\n" + "="*60)
print("Use the model that works above!")