# agente.py - Step 5 (LangChain 1.x): agente che decide da solo quando cercare.
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain.agents import create_agent   # <-- nuova API di LangChain 1.x

load_dotenv()  # carica il token HF dal .env

# 1) Riapro il DB Chroma e creo il retriever.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

# 2) Il TOOL che l'agente puo' decidere di usare (la docstring gli dice a cosa serve).
@tool
def cerca_documenti(domanda: str) -> str:
    """Cerca nei documenti aziendali le informazioni utili a rispondere a una domanda."""
    docs = retriever.invoke(domanda)
    return "\n\n".join(d.page_content for d in docs)

# 3) L'LLM (deve supportare il tool calling: Qwen2.5-Instruct lo fa).
motore = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct", task="text-generation")
llm = ChatHuggingFace(llm=motore)

# 4) Creo l'agente: modello + strumenti + istruzioni. Niente AgentExecutor.
agente = create_agent(
    model=llm,
    tools=[cerca_documenti],
    system_prompt=(
        "Sei DocBuddy, un assistente. Usa lo strumento cerca_documenti quando la "
        "domanda riguarda informazioni contenute nei documenti. Per i saluti o le "
        "chiacchiere, rispondi direttamente senza cercare."
    ),
)

# 5) Funzione comoda per fare una domanda all'agente.
def chiedi(testo):
    # L'agente vuole una lista di "messages" in stile chat.
    risultato = agente.invoke({"messages": [{"role": "user", "content": testo}]})
    # La risposta finale e' l'ultimo messaggio della conversazione.
    return risultato["messages"][-1].content

# 6) Provo due domande: una che richiede i documenti, una no.
print("=== Domanda 1 (dovrebbe cercare) ===")
print(chiedi("What do the documents say about this topic?"))

print("\n=== Domanda 2 (chiacchiera) ===")
print(chiedi("how is 30 x 5?"))