"""Prova: inserisce un utente e lo rilegge dal database."""
from database import SessionLocal
from models import User


def main():
    db = SessionLocal()
    try:
        # 1) Inserisco un nuovo utente
        nuovo = User(email="test@securedocs.dev")
        db.add(nuovo)
        db.commit()          # salva davvero nel DB
        db.refresh(nuovo)    # ricarica l'oggetto (ora ha id e created_at)
        print(f"Inserito: {nuovo}")

        # 2) Lo rileggo dal database
        letto = db.query(User).filter(User.email == "test@securedocs.dev").first()
        print(f"Riletto: {letto} | creato il {letto.created_at}")

        print("OK: scrittura e lettura riuscite.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
