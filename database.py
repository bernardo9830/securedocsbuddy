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

# L'engine e' la "presa di corrente" verso il database.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,                 # verifica la connessione prima di usarla
    connect_args={"connect_timeout": 5},  # non restare appeso se il DB non risponde
)

# SessionLocal e' la "fabbrica" di sessioni: ogni sessione e' una conversazione col DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base: la classe madre da cui erediteranno tutti i modelli (stile dichiarativo moderno).
class Base(DeclarativeBase):
    pass
