import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Carica le variabili dal file .env (tra cui DATABASE_URL)
load_dotenv()

# URL di connessione: preso da .env, con fallback locale se manca.
# Struttura: postgresql+psycopg2://UTENTE:PASSWORD@HOST:PORTA/NOME_DB
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://securedocs:devpassword@localhost:5432/securedocs",
)

# Le piattaforme cloud (Render, ecc.) danno un URL "postgres://..." o "postgresql://..."
# senza driver: lo normalizziamo per usare sempre psycopg2.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg2" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# Argomenti di connessione diversi a seconda del database.
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}   # SQLite con piu' thread
elif DATABASE_URL.startswith("postgresql"):
    connect_args = {"connect_timeout": 5}          # Postgres: fail-fast
else:
    connect_args = {}

# L'engine e' la "presa di corrente" verso il database.
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, connect_args=connect_args)

# SessionLocal e' la "fabbrica" di sessioni: ogni sessione e' una conversazione col DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base: la classe madre da cui erediteranno tutti i modelli (stile dichiarativo moderno).
class Base(DeclarativeBase):
    pass
