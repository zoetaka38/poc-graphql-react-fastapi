import strawberry

from app.graphql.scalars.stickynotes_scalar import (
    StickyNoteDeleted,
    StickyNoteNotFound,
    StickyNoteScalar,
)
from app.graphql.scalars.user_scalar import UserNameMissing, UserNotFound

AddStickyNotesResponse = strawberry.union("AddStickyNotesResponse", (StickyNoteScalar, UserNotFound, UserNameMissing))
UpdateStickyNotesResponse = strawberry.union("UpdateStickyNotesResponse", (StickyNoteScalar, StickyNoteNotFound))
DeleteStickyNotesResponse = strawberry.union("DeleteStickyNotesResponse", (StickyNoteDeleted, StickyNoteNotFound))
