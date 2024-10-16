from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .stickynotes import StickyNote  # noqa: F401

from . import Base  # noqa: E402

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column("name", String, nullable=False, unique=True)

    stickynotes: Mapped[list[StickyNote]] = relationship(
        "StickyNote",
        back_populates="user",
        foreign_keys="StickyNote.user_id",
        cascade="all, delete",
        passive_deletes=True,
    )

    def as_dict(self):
        return {"id": self.id, "name": self.name}
