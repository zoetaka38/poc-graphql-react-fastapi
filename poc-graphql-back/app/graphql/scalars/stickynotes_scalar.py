from dataclasses import field
from datetime import datetime

import strawberry


@strawberry.type
class StickyNoteScalar:
    id: int
    text: str = ""
    created_datetime: datetime | None = field(default_factory=datetime.now)
    user_id: int | None = None


@strawberry.type
class StickyNoteNotFound:
    message: str = "Couldn't find sticky notes with the supplied id"


@strawberry.type
class StickyNoteDeleted:
    message: str = "Sticky Notes deleted"
