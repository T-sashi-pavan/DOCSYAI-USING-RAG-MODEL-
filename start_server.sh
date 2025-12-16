#!/bin/bash
# Start RAG backend server (Git Bash compatible)

echo "Starting RAG backend server on localhost:8001..."
echo ""

cd "/c/Desktop/MACHINE LEARNING/RAG MODEL/ragbackend"

# Use the virtual environment Python
"/c/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
