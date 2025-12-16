@echo off
REM Windows batch script for testing RAG API endpoints
REM Run this after starting the backend server on port 8001

echo ======================================================================
echo RAG SYSTEM - CURL TEST SUITE
echo ======================================================================
echo.

REM Set the API base URL
set API_BASE=http://localhost:8001

echo Testing local server at: %API_BASE%
echo.

REM Test 1: Root endpoint
echo ----------------------------------------------------------------------
echo TEST 1: Root Endpoint
echo ----------------------------------------------------------------------
curl -s %API_BASE%/
echo.
echo.

REM Test 2: Stats endpoint
echo ----------------------------------------------------------------------
echo TEST 2: Stats Endpoint
echo ----------------------------------------------------------------------
curl -s %API_BASE%/stats
echo.
echo.

REM Test 3: General question (no PDF)
echo ----------------------------------------------------------------------
echo TEST 3: General Knowledge Question
echo ----------------------------------------------------------------------
curl -s -X POST %API_BASE%/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is machine learning?\",\"top_k\":5,\"threshold\":0.7}"
echo.
echo.

REM Test 4: Upload PDF (if test.pdf exists)
echo ----------------------------------------------------------------------
echo TEST 4: PDF Upload
echo ----------------------------------------------------------------------
if exist "test.pdf" (
    echo Uploading test.pdf...
    curl -s -X POST %API_BASE%/upload ^
      -F "file=@test.pdf" ^
      -H "accept: application/json"
    echo.
) else (
    echo ⚠️  test.pdf not found. Skipping upload test.
    echo Create a test.pdf file in this directory to test PDF upload.
)
echo.

echo ======================================================================
echo Test suite completed!
echo ======================================================================
echo.
echo 📝 Next steps:
echo 1. If tests failed, check:
echo    - Server is running on port 8001
echo    - API keys are set in .env file
echo 2. For PDF upload test, create test.pdf in current directory
echo 3. Open browser to http://localhost:8001/static/index.html
echo ======================================================================

pause
