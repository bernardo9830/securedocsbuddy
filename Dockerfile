# Immagine di base: Python leggero
FROM python:3.12-slim

# Cartella di lavoro dentro il container
WORKDIR /app

# Installo prima le dipendenze (sfrutta la cache di Docker se non cambiano)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copio il codice dell'app e il database vettoriale gia' costruito
COPY app.py .
COPY chroma_db ./chroma_db

# La porta su cui gira uvicorn dentro il container
EXPOSE 8000

# Comando di avvio: host 0.0.0.0 per essere raggiungibili dall'esterno
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
