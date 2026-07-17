# SecureDocs - Sprints

## Sprint 6 - Deploy cloud (URL pubblico + Postgres gestito)

Obiettivo sprint: mettere SecureDocs online, raggiungibile via HTTPS pubblico, con database Postgres gestito. Tutto su tier gratuiti.

### Vincolo tecnico da affrontare
- L'app carica gli embeddings in locale con `sentence-transformers` (riga 25 di `app.py`), che tira dentro `torch` (~2 GB tra libreria e runtime, picchi di RAM alti).
- I tier gratuiti (Render free = 512 MB RAM) NON reggono torch -> crash OOM all'avvio. Un deploy "as-is" fallirebbe.
- Soluzione: refactoring "cloud-light" -> spostare gli embeddings sull'Inference API di HuggingFace (chiamata al modello sul cloud HF via token, senza scaricarlo). Si rimuove torch dalle dipendenze e l'app diventa leggera.

### Task
- [ ] 6.1 Refactoring cloud-light: embeddings via HuggingFace Inference API (rimuove torch) - STATO: da iniziare
- [ ] 6.2 Reindicizzazione Chroma con lo stesso metodo di embedding via API - STATO: bloccato da 6.1
- [ ] 6.3 Deploy su Render: Postgres gestito + Web Service collegato al repo GitHub - STATO: bloccato da 6.1/6.2
- [ ] 6.4 Env/secret su Render (DATABASE_URL, SECRET_KEY, HUGGINGFACEHUB_API_TOKEN) + init_db sul DB gestito - STATO: bloccato da 6.3
- [ ] 6.5 Verifica: URL pubblico https risponde su /ping e /docs - STATO: bloccato da 6.4

### Skill coinvolte (da Skill Matrix)
- Deploy L2 (guidato), RAG & Embeddings L2, Chroma L2 -> affiancamento medio
- SQL/PostgreSQL L0 -> molto affiancamento sulla parte DB gestito
- CI/CD L0 -> Render fa build automatica dal repo, niente pipeline da scrivere ora
