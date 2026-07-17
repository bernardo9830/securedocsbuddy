from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = "users"  # nome della tabella nel database

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    # placeholder: NON e' ancora una password reale, la gestiremo nello Sprint 3
    hashed_password: Mapped[str] = mapped_column(String(255), default="placeholder")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
