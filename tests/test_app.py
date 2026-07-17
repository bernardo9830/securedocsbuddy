# tests/test_app.py
# Primi test automatici di SecureDocs.
# Testiamo SOLO endpoint che NON chiamano l'LLM o la rete,
# cosi' i test sono veloci, stabili e non consumano token HF.

from fastapi.testclient import TestClient

# NOTA: importare "app" esegue il codice a livello di modulo di app.py,
# incluso il caricamento degli embeddings e la creazione del client LLM.
# Quindi il PRIMO avvio dei test e' un po' lento. Va bene: i nostri test
# toccano solo endpoint "leggeri" che non invocano l'LLM.
from app import app

# Il TestClient simula un client HTTP senza avviare davvero uvicorn.
client = TestClient(app)


def test_ping():
    """GET /ping deve rispondere 200 e il JSON {"messaggio": "pong"}."""
    risposta = client.get("/ping")
    assert risposta.status_code == 200
    assert risposta.json() == {"messaggio": "pong"}


def test_home_html():
    """GET / deve rispondere 200 e restituire la pagina HTML."""
    risposta = client.get("/")
    assert risposta.status_code == 200
    assert "DocBuddy" in risposta.text


def test_download_inesistente():
    """GET /download con un nome inesistente deve dare 404."""
    risposta = client.get("/download/file_che_non_esiste.docx")
    assert risposta.status_code == 404