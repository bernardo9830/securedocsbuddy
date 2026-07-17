# rag.py - Step 4: catena RAG completa (retriever + LLM) con citazione delle fonti.
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()  # carica il token HF dal .env

# 1) Riapro il DB Chroma gia' creato nello step 3C (STESSO modello di embedding!).
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# 2) Il retriever: dato un testo, pesca i k documenti piu' vicini dal DB.
retriever = db.as_retriever(search_kwargs={"k": 3})

# 3) L'LLM (lo stesso modellino dello step 3A).
motore = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct", task="text-generation")
llm = ChatHuggingFace(llm=motore)

# 4) Il prompt: dice all'LLM di rispondere USANDO SOLO il contesto fornito.
prompt = ChatPromptTemplate.from_template(
    "Rispondi alla domanda usando SOLO il contesto qui sotto. "
    "Se la risposta non c'e' nel contesto, dillo chiaramente.\n\n"
    "Contesto:\n{context}\n\n"
    "Domanda: {input}\n\n"
    "Risposta:"
)

# 5) Costruisco la catena:
#    - create_stuff_documents_chain: infila i documenti recuperati dentro il prompt
#    - create_retrieval_chain: collega il retriever alla catena precedente
combina = create_stuff_documents_chain(llm, prompt)
rag = create_retrieval_chain(retriever, combina)

# 6) Faccio una domanda. CAMBIALA con una domanda vera sui tuoi documenti:
#    (nello step 3C hai visto delle "domanda collegata": puoi copiarne una qui)
domanda = "What is the main topic discussed in the documents?"
risposta = rag.invoke({"input": domanda})

print("DOMANDA:", domanda)
print("\nRISPOSTA:\n", risposta["answer"])

# 7) Mostro le FONTI usate (i documenti recuperati dal DB).
print("\n--- FONTI USATE ---")
for i, doc in enumerate(risposta["context"], start=1):
    print(f"[{i}] id={doc.metadata.get('id')} | domanda collegata: {doc.metadata.get('domanda')}")