# indicizza.py - Step 3C: crea gli embeddings e li salva nel DB vettoriale Chroma.
import os
from dotenv import load_dotenv
from datasets import load_dataset
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()  # carica HUGGINGFACEHUB_API_TOKEN dal .env

# 1) Ricreo i documenti dal dataset (come nello step 3B).
dataset = load_dataset("neural-bridge/rag-dataset-1200", split="train")
subset = dataset.select(range(200))
documenti = [
    Document(page_content=r["context"], metadata={"id": i, "domanda": r["question"]})
    for i, r in enumerate(subset)
]
print(f"Documenti da indicizzare: {len(documenti)}")

# 2) Embeddings via HuggingFace Inference API (stesso metodo dell'app, niente torch).
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

# 3) Creo il DB vettoriale Chroma e ci carico i documenti (calcola gli embeddings).
#    persist_directory = la cartella su disco dove Chroma salva il database.
db = FAISS.from_documents(documenti, embeddings)
db.save_local("faiss_index")
print("Indice FAISS creato e salvato in ./faiss_index")

# 4) Prova: cerco i documenti piu' vicini a una domanda (similarity search).
#    Uso la domanda del primo documento: dovrei ritrovarlo tra i risultati.
domanda = documenti[0].metadata["domanda"]
risultati = db.similarity_search(domanda, k=3)  # k = quanti risultati
print(f"\n--- Top 3 risultati per: {domanda} ---")
for i, doc in enumerate(risultati, start=1):
    print(f"\n[{i}] {doc.page_content[:200]} ...")