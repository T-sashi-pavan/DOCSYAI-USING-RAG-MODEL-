#!/bin/bash
# Git Bash compatible test script for RAG API

echo "======================================================================"
echo "RAG SYSTEM - API TEST SUITE (Git Bash)"
echo "======================================================================"
echo ""

API_BASE="http://localhost:8001"

echo "Testing server at: $API_BASE"
echo ""

# Test 1: Root endpoint
echo "----------------------------------------------------------------------"
echo "TEST 1: Root Endpoint"
echo "----------------------------------------------------------------------"
curl -s $API_BASE/
echo ""
echo ""

# Test 2: Stats endpoint
echo "----------------------------------------------------------------------"
echo "TEST 2: Stats Endpoint"
echo "----------------------------------------------------------------------"
curl -s $API_BASE/stats
echo ""
echo ""

# Test 3: General question (no PDF)
echo "----------------------------------------------------------------------"
echo "TEST 3: General Knowledge Question (No PDF)"
echo "----------------------------------------------------------------------"
curl -s -X POST $API_BASE/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is machine learning?","top_k":5,"threshold":0.7}'
echo ""
echo ""

# Test 4: Upload PDF
echo "----------------------------------------------------------------------"
echo "TEST 4: PDF Upload"
echo "----------------------------------------------------------------------"
if [ -f "test.pdf" ]; then
    echo "Uploading test.pdf..."
    curl -s -X POST $API_BASE/upload \
      -F "file=@test.pdf" \
      -H "accept: application/json"
    echo ""
    echo ""
    
    # Wait a bit for processing
    echo "Waiting 3 seconds for PDF processing..."
    sleep 3
    
    # Test 5: Question about PDF
    echo "----------------------------------------------------------------------"
    echo "TEST 5: Question About Uploaded PDF"
    echo "----------------------------------------------------------------------"
    curl -s -X POST $API_BASE/ask \
      -H "Content-Type: application/json" \
      -d '{"question":"What are the types of machine learning mentioned in the document?","top_k":5,"threshold":0.7}'
    echo ""
    echo ""
else
    echo "⚠️  test.pdf not found. Skipping upload test."
    echo ""
fi

echo "======================================================================"
echo "✅ Test suite completed!"
echo "======================================================================"
echo ""
echo "📝 Next steps:"
echo "1. Check the responses above"
echo "2. Open browser: file:///C:/Desktop/MACHINE%20LEARNING/RAG%20MODEL/ragbackend/static/index.html"
echo "3. Upload test.pdf and ask questions"
echo "======================================================================"
