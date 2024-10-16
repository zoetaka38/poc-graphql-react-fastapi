import strawberry

from app.graphql.scalars.user_scalar import (
    AddUser,
    UserDeleted,
    UserExists,
    UserIdMissing,
    UserNotFound,
)

AddUserResponse = strawberry.union("AddUserResponse", (AddUser, UserExists))
DeleteUserResponse = strawberry.union(
    "DeleteUserResponse", (UserDeleted, UserNotFound, UserIdMissing)
)
