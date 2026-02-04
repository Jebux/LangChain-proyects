import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import shutil

# Directory to persist the vector database
PERSIST_DIRECTORY = "./data/chroma_db"
# Directory to save uploaded files temporarily
UPLOAD_DIRECTORY = "./data/uploads"

os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def get_vectorstore():
    """Returns the Chroma vector store instance."""
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="agent_docs"
    )
    return vectorstore

def ingest_document(file_path: str, filename: str):
    """Parses a PDF or Text file and adds it to the vector store."""
    if filename.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        # Assume text file
        loader = TextLoader(file_path)
    
    docs = loader.load()
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Add to vector store
    vectorstore = get_vectorstore()
    vectorstore.add_documents(splits)
    
    return len(splits)

def get_retriever_tool_func():
    """Creates a LangChain tool for the agent to retrieve information."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()
    tool = create_retriever_tool(
        retriever,
        "search_uploaded_docs",
        "Searches and returns excerpts from the uploaded documents. "
        "Use this tool when the user asks questions about specific documents or content they have uploaded."
    )
    return tool
