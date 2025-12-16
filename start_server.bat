@echo off
echo Starting RAG backend server on localhost:8001...
echo.
cd /d "C:\Desktop\MACHINE LEARNING\RAG MODEL\ragbackend"
"C:/Desktop/MACHINE LEARNING/RAG MODEL/.venv/Scripts/python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
