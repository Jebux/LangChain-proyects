from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from app.rag import ingest_document, UPLOAD_DIRECTORY
from app.agent import get_agent_executor
from app.models import ChatRequest, ChatResponse, UploadResponse

app = FastAPI(title="AI Agent Backend", version="1.0")

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
    """Endpoint to interact with the AI Agent."""
    try:
        executor = get_agent_executor()
        
        # Invoke agent
        result = executor.invoke({"input": request.message})
        
        return ChatResponse(response=result["output"])
    except Exception as e:
        print(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
