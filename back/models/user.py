from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(unique=True, nullable=False)
    pswd_hashed: Mapped[str] = mapped_column(nullable=False)

    notes_owned: Mapped[list["Note"]] = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
