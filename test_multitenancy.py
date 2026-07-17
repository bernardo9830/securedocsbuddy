from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_chiedi_richiede_login():
    # Nessun header Authorization => deve essere rifiutato.
    resp = client.post("/chiedi", json={"domanda": "ciao"})
    assert resp.status_code in (401, 403)


def test_svuota_memoria_richiede_login():
    resp = client.post("/svuota-memoria")
    assert resp.status_code in (401, 403)
