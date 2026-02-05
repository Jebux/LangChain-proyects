from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import shutil
import os
import json
from app.rag import ingest_document, UPLOAD_DIRECTORY
from app.agent_enhanced import invoke_agent_with_streaming, invoke_agent_sync
from app.models import ChatRequest, ChatResponse, UploadResponse

app = FastAPI(title="AI Agent Backend", version="2.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Agent Backend is running"}

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Endpoint to upload PDF or Text files for RAG."""
    allowed_extensions = [".pdf", ".txt"]
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger Ingestion
        num_chunks = ingest_document(file_path, filename)
        
        return UploadResponse(
            filename=filename, 
            status="success", 
            message=f"File uploaded and vectorized successfully. Added {num_chunks} chunks."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to interact with the AI Agent (Non-streaming).
    Uses enhanced LangGraph agent with state persistence.
    """
    try:
        # Use enhanced agent with checkpointing
        response_text = invoke_agent_sync(
            user_input=request.message,
            thread_id=request.session_id or "default_session"
        )
        
        # invoke_agent_sync already returns a clean string
        return ChatResponse(response=response_text)
        
    except Exception as e:
        print(f"Error during chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Endpoint to interact with the AI Agent with streaming responses.
    Uses enhanced LangGraph agent with state persistence and streaming.
    
    Returns Server-Sent Events (SSE) stream.
    """
    try:
        async def generate():
            """Generator for streaming responses."""
            full_response = ""
            
            async for chunk in invoke_agent_with_streaming(
                user_input=request.message,
                thread_id=request.session_id or "default_session"
            ):
                if chunk:
                    full_response += chunk
                    # Send chunk as SSE
                    yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
            
            # Send final message
            yield f"data: {json.dumps({'chunk': '', 'done': True, 'full_response': full_response})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )
    except Exception as e:
        print(f"Error during streaming chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
