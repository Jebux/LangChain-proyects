from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

#importa el modelo de embeddings y la base de datos FAISS
embeddings = OpenAIEmbeddings()
db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)

# Realiza una búsqueda de similitud con una consulta de ejemplo
# Trae los 3 documentos más similares (k=3)
query = "What are the payment terms?"
docs = db.similarity_search(query, k=3)

# Imprime los documentos recuperados (no necesario para el RAG, solo para ver qué se recuperó)
for d in docs:
    print(d.page_content)

from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje
llm = ChatOpenAI()

# Crea el contexto a partir de los documentos recuperados
context = "\n\n".join([d.page_content for d in docs])

# Crea el prompt para la respuesta basada en el contexto
prompt = f"""
Answer ONLY using the following context:

{context}

Question:
Who was albert einstein?
"""

# Genera la respuesta utilizando el modelo de lenguaje
response = llm.invoke(prompt)
print(response.content)
