from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User

from . import Base  # noqa: E402


class StickyNote(Base):
    __tablename__ = "stickynote"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column("text", String, nullable=True)
    created_datetime: Mapped[DateTime] = mapped_column("created_datetime", DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    user: Mapped[User] = relationship("User", back_populates="stickynotes", foreign_keys=[user_id])

    def as_dict(self):
        return {"id": self.id, "text": self.text, "created_datetime": self.created_datetime, "user_id": self.user_id}
