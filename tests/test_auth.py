import uuid
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_flusso_auth():
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    pwd = "SuperSegreta123"

    r = client.post("/registrazione", json={"email": email, "password": pwd})
    assert r.status_code == 201

    r = client.post("/login", data={"username": email, "password": pwd})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == email

    # Senza token -> negato
    assert client.get("/me").status_code == 401
