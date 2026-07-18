# Dockerfile per Hugging Face Spaces (16 GB RAM gratis).
FROM python:3.12-slim

WORKDIR /app

# Dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codice + indice FAISS + tutto il resto (segreti esclusi da .dockerignore)
COPY . .

# Cartella scrivibile per i file generati (Word/PPT)
RUN mkdir -p /app/downloads && chmod -R 777 /app/downloads

# HF Spaces instrada sulla porta 7860
EXPOSE 7860
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
