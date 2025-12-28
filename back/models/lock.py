from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey

from models import db


class Lock(db.Model):
    __tablename__ = "locks"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    note: Mapped["Note"] = relationship("Note", back_populates="lock")
