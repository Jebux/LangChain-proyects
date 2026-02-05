import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
import shutil
import traceback

load_dotenv()

# Directories
UPLOAD_DIRECTORY = "./uploaded_docs"
CHROMA_PERSIST_DIR = "./chroma_db"

# Create directories if they don't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Initialize embeddings
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
)

# Global vectorstore instance
_vectorstore = None

def reset_chroma_db():
    """Completely reset ChromaDB by deleting and recreating the directory."""
    global _vectorstore
    _vectorstore = None
    
    try:
        if os.path.exists(CHROMA_PERSIST_DIR):
            print(f"🗑️  Deleting existing ChromaDB at: {CHROMA_PERSIST_DIR}")
            shutil.rmtree(CHROMA_PERSIST_DIR)
        
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        print(f"✅ Created fresh ChromaDB directory: {CHROMA_PERSIST_DIR}")
        
    except Exception as e:
        print(f"❌ Error resetting ChromaDB: {e}")
        traceback.print_exc()
        raise

def get_vector_store():
    """Get or create vector store with proper error handling."""
    global _vectorstore
    
    if _vectorstore is not None:
        return _vectorstore
    
    try:
        print(f"🔄 Initializing ChromaDB at: {CHROMA_PERSIST_DIR}")
        
        # Ensure directory exists
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        
        _vectorstore = Chroma(
            collection_name="uploaded_documents",
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        print(f"✅ ChromaDB initialized successfully")
        return _vectorstore
        
    except KeyError as e:
        if "'_type'" in str(e):
            print(f"❌ ChromaDB corruption detected (KeyError: '_type'). Resetting...")
            reset_chroma_db()
            
            # Recreate after reset
            _vectorstore = Chroma(
                collection_name="uploaded_documents",
                embedding_function=embeddings,
                persist_directory=CHROMA_PERSIST_DIR
            )
            print(f"✅ ChromaDB recreated after reset")
            return _vectorstore
        else:
            raise
            
    except Exception as e:
        print(f"❌ Error initializing ChromaDB: {e}")
        traceback.print_exc()
        
        # Try reset as last resort
        print("🔄 Attempting full reset...")
        reset_chroma_db()
        
        _vectorstore = Chroma(
            collection_name="uploaded_documents",
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        print(f"✅ ChromaDB created after reset")
        return _vectorstore

def ingest_document(file_path: str, filename: str) -> int:
    """
    Load, split, and store a document into the vector database.
    Returns the number of chunks created.
    """
    try:
        print(f"\n{'='*60}")
        print(f"📄 Starting Document Ingestion")
        print(f"   File: {filename}")
        print(f"   Path: {file_path}")
        print(f"{'='*60}")
        
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        print(f"📊 File size: {file_size:,} bytes")
        
        ext = os.path.splitext(filename)[1].lower()
        
        # Load document
        print(f"🔄 Loading document ({ext})...")
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} page(s)/section(s)")
        
        if not documents:
            raise ValueError("No content could be extracted from the document")
        
        # Add filename to metadata
        for doc in documents:
            doc.metadata["source"] = filename
        
        # Split documents
        print(f"🔄 Splitting into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        if not chunks:
            raise ValueError("Document splitting produced no chunks")
        
        # Store in vector database
        print(f"🔄 Storing in ChromaDB...")
        vectorstore = get_vector_store()
        vectorstore.add_documents(chunks)
        
        print(f"{'='*60}")
        print(f"✅ Ingestion Complete: {len(chunks)} chunks from {filename}")
        print(f"{'='*60}\n")
        
        return len(chunks)
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ INGESTION FAILED")
        print(f"   Error: {e}")
        print(f"{'='*60}\n")
        traceback.print_exc()
        raise

def get_retriever_tool_func():
    """
    Returns a LangChain Tool that wraps the retriever for OpenAI Tools Agent.
    """
    vectorstore = get_vector_store()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="search_uploaded_docs",
        description=(
            "Search for information in uploaded documents. "
            "Input should be a clear search query or question. "
            "Returns relevant text passages from the documents."
        )
    )
    
    return retriever_tool
