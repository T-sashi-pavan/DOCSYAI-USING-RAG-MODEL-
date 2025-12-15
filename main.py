from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.rag_system import RAGSystem
import os
import shutil
import traceback
import asyncio
import json 

app = FastAPI(title="PDF Q&A API")

# Serve static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system with error handling
try:
    rag = RAGSystem(collection_name="pdf_qa_collection")
    print("✅ RAG System initialized successfully")
except Exception as e:
    print(f" Failed to initialize RAG System: {str(e)}")
    print(traceback.format_exc())
    rag = None

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5
    threshold: float = 0.7

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend interface."""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "PDF Q&A API", "status": "running", "note": "Frontend not found. API is working."}

@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {"message": "PDF Q&A API", "status": "running"}

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    health = {
        "status": "ok",
        "rag_initialized": rag is not None,
        "environment_variables": {
            "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY")),
            "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
            "SUPABASE_URL": bool(os.getenv("SUPABASE_URL")),
            "SUPABASE_ANON_KEY": bool(os.getenv("SUPABASE_ANON_KEY"))
        }
    }
    
    if rag:
        try:
            health["document_count"] = rag.vector_store.count_documents()
        except Exception as e:
            health["document_count_error"] = str(e)
    
    return health

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """Upload PDF and process in background for faster response."""
    
    # Check if RAG is initialized
    if rag is None:
        raise HTTPException(500, "RAG system not initialized. Check environment variables.")
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    
    # Save uploaded file
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    
    try:
        # Save file asynchronously
        print(f"📥 Saving file: {file.filename}")
        contents = await file.read()
        
        # Write file in background
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: open(file_path, "wb").write(contents))
        print(f"✅ File saved: {file_path}")
        
        # Add PDF processing as background task (non-blocking)
        background_tasks.add_task(_process_pdf_background, file_path, file.filename)
        
        return {
            "status": "processing",
            "filename": file.filename,
            "message": "PDF is being processed. Query the /stats endpoint to check progress."
        }
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ Error saving PDF:")
        print(error_trace)
        raise HTTPException(500, f"Error saving PDF: {str(e)}")


def _process_pdf_background(file_path: str, filename: str):
    """Process PDF in background with memory cleanup."""
    try:
        print(f"📄 Processing PDF in background: {filename}")
        rag.ingest_pdf(file_path)
        print(f"✅ PDF processed successfully: {filename}")
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ Error processing PDF in background:")
        print(error_trace)
    finally:
        # Aggressive cleanup
        import gc
        gc.collect()
        
        # Clean up file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Temporary file removed")
            except:
                pass

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded PDFs."""
    if rag is None:
        raise HTTPException(500, "RAG system not initialized")
    
    try:
        print(f"❓ Question received: {request.question}")
        
        # Run blocking RAG operations in executor (non-blocking)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            rag.ask,
            request.question,
            request.top_k,
            request.threshold
        )
        print(f"✅ Answer generated")
        return response
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ Error generating answer:")
        print(error_trace)
        raise HTTPException(500, f"Error generating answer: {str(e)}")


@app.post("/ask-stream")
async def ask_question_streaming(request: QuestionRequest):
    """Ask a question with streaming answer for real-time response."""
    if rag is None:
        raise HTTPException(500, "RAG system not initialized")
    
    async def generate():
        try:
            # Run blocking operations in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                rag.ask,
                request.question,
                request.top_k,
                request.threshold
            )
            
            # Stream the response in chunks
            yield json.dumps({"status": "answer_start", "answer_part": ""}).encode() + b"\n"
            
            answer = response.get('answer', '')
            # Stream answer in chunks for better UX
            chunk_size = 50
            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i+chunk_size]
                yield json.dumps({"status": "answer_chunk", "answer_part": chunk}).encode() + b"\n"
                await asyncio.sleep(0.01)  # Small delay for streaming effect
            
            # Send metadata
            response['answer'] = answer  # Include full answer in metadata
            yield json.dumps({"status": "complete", "metadata": response}).encode() + b"\n"
        except Exception as e:
            yield json.dumps({"status": "error", "error": str(e)}).encode() + b"\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    if rag is None:
        raise HTTPException(500, "RAG system not initialized")
    
    try:
        stats = rag.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(500, f"Error fetching stats: {str(e)}")

@app.delete("/clear")
async def clear_database():
    """Clear all documents from database."""
    if rag is None:
        raise HTTPException(500, "RAG system not initialized")
    
    try:
        rag.vector_store.clear()
        return {"status": "success", "message": "Database cleared"}
    except Exception as e:
        raise HTTPException(500, f"Error clearing database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)