# ingest.py - Step 3B: scarica un dataset di documenti e li prepara per il RAG.
from datasets import load_dataset
from langchain_core.documents import Document

# Scarico il dataset RAG di neural-bridge.
# Ogni riga ha: "context" (il documento), "question", "answer".
dataset = load_dataset("neural-bridge/rag-dataset-1200", split="train")
print(f"Righe totali nel dataset: {len(dataset)}")

# Per iniziare leggeri, prendo solo le prime 200 righe (embeddare tutto e' piu' lento).
subset = dataset.select(range(200))

# Trasformo ogni "context" in un Document di LangChain.
# Nel metadata tengo un id e la domanda collegata: serviranno per le citazioni.
documenti = []
for i, riga in enumerate(subset):
    documenti.append(
        Document(
            page_content=riga["context"],
            metadata={"id": i, "domanda": riga["question"]},
        )
    )

print(f"Documenti creati: {len(documenti)}")
print("\n--- Esempio di documento ---")
print(documenti[0].page_content[:400], "...")
print("\nMetadata:", documenti[0].metadata)