from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  ForeignKey, Text, func, Enum as SQLEnum

from models import db
class Note(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    visibility: Mapped[str] = mapped_column(
        SQLEnum("private", "read", "write", name="note_visibility", native_enum=False),
        nullable=False,
        default="private",
    )
    created_at: Mapped[str] = mapped_column(server_default=func.current_date(), nullable=False)
    updated_at: Mapped[str] = mapped_column(server_default=func.current_date(), onupdate=func.current_date(), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="notes_owned")
    lock: Mapped["Lock"] = relationship("Lock", back_populates="note", uselist=False, cascade="all, delete-orphan")
