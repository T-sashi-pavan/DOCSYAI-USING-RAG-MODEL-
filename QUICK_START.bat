@echo off
echo ======================================================================
echo RAG SYSTEM - QUICK START GUIDE
echo ======================================================================
echo.
echo Current Status:
echo   Memory Usage: 71 MB / 512 MB (14%% - EXCELLENT!)
echo   Frontend: Auto-detects local vs production
echo   Backend: Ready to run on port 8001
echo   Test PDF: Created and ready
echo.
echo ======================================================================
echo REQUIRED: API KEYS (Get these first!)
echo ======================================================================
echo.
echo 1. COHERE API KEY (for embeddings):
echo    - Go to: https://dashboard.cohere.com/api-keys
echo    - Sign up for FREE
echo    - Copy your key
echo    - Add to .env: COHERE_API_KEY=your_key
echo.
echo 2. SUPABASE ANON KEY (for vector database):
echo    - Go to: https://app.supabase.com/project/hjzalxzfgtbrokhdxhkt/settings/api
echo    - Copy the 'anon' 'public' key (starts with eyJ...)
echo    - Add to .env: SUPABASE_ANON_KEY=your_key
echo.
echo ======================================================================
echo QUICK START - 3 SIMPLE STEPS
echo ======================================================================
echo.
echo Step 1: Edit .env file and add API keys
echo    notepad .env
echo.
echo Step 2: Start the backend server
echo    CALL start_server.bat
echo.
echo Step 3: Open browser and test
echo    - Open: static\index.html
echo    - Upload: test.pdf
echo    - Ask: "What is machine learning?"
echo.
echo ======================================================================
echo FULL TESTING COMMANDS
echo ======================================================================
echo.
echo Memory test (no API keys needed):
echo    python test_memory.py
echo.
echo API endpoint tests:
echo    CALL test_api.bat
echo.
echo Browser test:
echo    start static\index.html
echo.
echo ======================================================================
echo DEPLOYMENT TO RENDER (After local testing succeeds)
echo ======================================================================
echo.
echo 1. Commit changes:
echo    git add .
echo    git commit -m "Ready for deployment"
echo    git push origin main
echo.
echo 2. Add API keys to Render environment variables
echo.
echo 3. Deploy and test at:
echo    https://docsyai-using-rag-model.onrender.com
echo.
echo ======================================================================
echo.
pause
