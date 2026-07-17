"""Crea tutte le tabelle definite nei modelli."""
from database import Base, engine
import models  # importa i modelli cosi' Base li "conosce"

if __name__ == "__main__":
    print("Creo le tabelle...")
    Base.metadata.create_all(bind=engine)
    print("Tabelle create con successo.")
