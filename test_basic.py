from src.rag_system import RAGSystem

print("=" * 60)
print("Testing PDF Q&A System with Groq")
print("=" * 60)

# Initialize system
rag = RAGSystem(collection_name="test_collection")

# Upload PDF
pdf_path = "data/sample.pdf"
print(f"\n📤 Uploading PDF: {pdf_path}")
rag.ingest_pdf(pdf_path)

# Ask questions
print("\n" + "=" * 60)
print("Asking Questions")
print("=" * 60)

questions = [
    "What is the main topic of this document?",
    "Can you summarize the key points?",
]

for question in questions:
    print(f"\n{'='*60}")
    response = rag.ask(question)
    print(f"Q: {question}")
    print(f"A: {response['answer']}")
    print(f"\nSources used: {len(response['sources'])}")

print("\n✅ Test complete!")