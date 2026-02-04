import requests
import os

BASE_URL = "http://localhost:8000"

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.json()}")
    except Exception as e:
        print(f"Failed to connect to root: {e}")

def test_upload():
    # Create a dummy file
    filename = "test_doc.txt"
    with open(filename, "w") as f:
        f.write("The capital of France is Paris. The AI agent backend was built with FastAPI.")
    
    try:
        with open(filename, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            print(f"Upload endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Failed to upload: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def test_chat():
    payload = {"message": "What is the capital of France?"}
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        print(f"Chat endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Failed to chat: {e}")

if __name__ == "__main__":
    print("Testing API...")
    test_root()
    test_upload()
    test_chat()
