# auth.py - Sicurezza: hashing password + creazione/validazione token JWT.
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

load_dotenv()  # carica SECRET_KEY dal .env

# --- Configurazione ---
SECRET_KEY = os.getenv("SECRET_KEY")  # chiave segreta per firmare i JWT
ALGORITHM = "HS256"                    # algoritmo di firma
DURATA_TOKEN_MINUTI = 60               # dopo 60 min il token scade

# Usiamo direttamente la libreria bcrypt (passlib non e' piu' mantenuta).

# Dice a FastAPI: il token arriva nell'header "Authorization: Bearer <token>".
# tokenUrl serve solo a Swagger per sapere dove fare il login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- Dependency: una sessione DB per ogni richiesta, chiusa a fine richiesta ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Password ---
def hash_password(password: str) -> str:
    """Trasforma la password in un'impronta bcrypt (irreversibile)."""
    # bcrypt lavora sui byte e ha un limite di 72 byte: tronchiamo per sicurezza.
    pwd_bytes = password.encode("utf-8")[:72]
    impronta = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return impronta.decode("utf-8")  # salviamo l'impronta come stringa


def verify_password(password_in_chiaro: str, hash_salvato: str) -> bool:
    """Confronta la password digitata con l'impronta salvata nel DB."""
    pwd_bytes = password_in_chiaro.encode("utf-8")[:72]
    return bcrypt.checkpw(pwd_bytes, hash_salvato.encode("utf-8"))


# --- Token JWT ---
def crea_token(dati: dict) -> str:
    """Crea un JWT firmato con una scadenza. In 'dati' mettiamo l'identita' (es. email)."""
    da_codificare = dati.copy()
    scadenza = datetime.now(timezone.utc) + timedelta(minutes=DURATA_TOKEN_MINUTI)
    da_codificare.update({"exp": scadenza})  # "exp" = quando scade
    return jwt.encode(da_codificare, SECRET_KEY, algorithm=ALGORITHM)


def decodifica_token(token: str) -> dict:
    """Verifica firma e scadenza del token; se non valido solleva un errore."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# --- Dependency: recupera l'utente corrente dal token ---
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Legge il token dall'header, lo valida e restituisce l'utente dal DB."""
    credenziali_invalide = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodifica_token(token)
        email = payload.get("sub")  # "sub" = soggetto (chi e')
        if email is None:
            raise credenziali_invalide
    except JWTError:
        raise credenziali_invalide

    utente = db.query(User).filter(User.email == email).first()
    if utente is None:
        raise credenziali_invalide
    return utente
