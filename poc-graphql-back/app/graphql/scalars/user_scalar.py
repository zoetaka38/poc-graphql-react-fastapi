from dataclasses import field

import strawberry

from app.graphql.scalars.stickynotes_scalar import StickyNoteScalar


@strawberry.type
class UserScalar:
    id: int
    name: str | None = ""
    stickynotes: list[StickyNoteScalar] = field(default_factory=list)


@strawberry.type
class AddUser:
    id: int
    name: str | None = ""


@strawberry.type
class UserExists:
    message: str = "User with this name already exists"


@strawberry.type
class UserNotFound:
    message: str = "Couldn't find user with the supplied id"


@strawberry.type
class UserNameMissing:
    message: str = "Please supply user name"


@strawberry.type
class UserIdMissing:
    message: str = "Please supply user id"


@strawberry.type
class UserDeleted:
    message: str = "User deleted"
