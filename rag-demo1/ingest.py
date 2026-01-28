from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Lee el archivo de texto
with open("data/docs.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Divide el texto en fragmentos manejables
# chunk_size es el tamaño máximo de cada fragmento
# chunk_overlap es la cantidad de superposición entre fragmentos
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# Crea los fragmentos de texto
chunks = splitter.split_text(text)

# Imprime la cantidad de fragmentos creados (para verificación)
print(f"Chunks created: {len(chunks)}")

from langchain_openai import OpenAIEmbeddings

# Crea los vectores de embeddings para cada fragmento de texto
embeddings = OpenAIEmbeddings()
vectors = embeddings.embed_documents(chunks)

print(len(vectors), len(vectors[0]))

from langchain_community.vectorstores import FAISS

# Crea y guarda la base de datos FAISS localmente
db = FAISS.from_texts(chunks, embeddings)
db.save_local("vector_index")
