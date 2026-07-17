# auth_router.py - Endpoint di registrazione, login e profilo protetto.
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from auth import (
    get_db,
    hash_password,
    verify_password,
    crea_token,
    get_current_user,
)
from models import User

router = APIRouter(tags=["auth"])


# --- Schemi (cosa entra/esce, senza mai esporre la password) ---
class RegistrazioneInput(BaseModel):
    email: EmailStr
    password: str


class UtenteOutput(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # permette di leggere direttamente dall'oggetto User


class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- POST /registrazione ---
@router.post("/registrazione", response_model=UtenteOutput, status_code=201)
def registrazione(dati: RegistrazioneInput, db: Session = Depends(get_db)):
    # Email gia' esistente? Blocco (email e' unica nel modello).
    if db.query(User).filter(User.email == dati.email).first():
        raise HTTPException(status_code=400, detail="Email gia' registrata")

    nuovo = User(
        email=dati.email,
        hashed_password=hash_password(dati.password),  # salvo SOLO l'impronta
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


# --- POST /login ---
# OAuth2PasswordRequestForm si aspetta i campi "username" e "password" (form).
# Qui "username" e' la nostra email.
@router.post("/login", response_model=TokenOutput)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    utente = db.query(User).filter(User.email == form.username).first()
    # Stesso messaggio per utente inesistente o password errata (non diamo indizi).
    if not utente or not verify_password(form.password, utente.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crea_token({"sub": utente.email})  # "sub" = email dell'utente
    return TokenOutput(access_token=token)


# --- GET /me (protetto) ---
@router.get("/me", response_model=UtenteOutput)
def me(utente_corrente: User = Depends(get_current_user)):
    # Se il token e' valido, get_current_user restituisce l'utente; altrimenti 401.
    return utente_corrente
