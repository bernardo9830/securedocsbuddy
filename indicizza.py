# indicizza.py - Step 3C: crea gli embeddings e li salva nel DB vettoriale Chroma.
from datasets import load_dataset
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1) Ricreo i documenti dal dataset (come nello step 3B).
dataset = load_dataset("neural-bridge/rag-dataset-1200", split="train")
subset = dataset.select(range(200))
documenti = [
    Document(page_content=r["context"], metadata={"id": i, "domanda": r["question"]})
    for i, r in enumerate(subset)
]
print(f"Documenti da indicizzare: {len(documenti)}")

# 2) Modello di embedding: gira in locale, gratis. Trasforma testo -> vettore.
#    all-MiniLM-L6-v2 e' piccolo e veloce (la prima volta lo scarica, ~90 MB).
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3) Creo il DB vettoriale Chroma e ci carico i documenti (calcola gli embeddings).
#    persist_directory = la cartella su disco dove Chroma salva il database.
db = Chroma.from_documents(
    documents=documenti,
    embedding=embeddings,
    persist_directory="chroma_db",
)
print("DB vettoriale creato e salvato in ./chroma_db")

# 4) Prova: cerco i documenti piu' vicini a una domanda (similarity search).
#    Uso la domanda del primo documento: dovrei ritrovarlo tra i risultati.
domanda = documenti[0].metadata["domanda"]
risultati = db.similarity_search(domanda, k=3)  # k = quanti risultati
print(f"\n--- Top 3 risultati per: {domanda} ---")
for i, doc in enumerate(risultati, start=1):
    print(f"\n[{i}] {doc.page_content[:200]} ...")