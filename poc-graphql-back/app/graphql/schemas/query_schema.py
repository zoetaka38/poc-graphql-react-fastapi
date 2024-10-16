import strawberry
from pydantic import typing
from strawberry.types import Info

from app.graphql.resolvers.stickynote_resolver import get_stickynote, get_stickynotes
from app.graphql.resolvers.user_resolver import get_user, get_users
from app.graphql.scalars.stickynotes_scalar import StickyNoteScalar
from app.graphql.scalars.user_scalar import UserScalar


@strawberry.type
class Query:

    @strawberry.field
    async def users(self, info: Info) -> list[UserScalar]:
        """Get all users"""
        users_data_list = await get_users(info)
        return users_data_list

    @strawberry.field
    async def user(self, info: Info, user_id: int) -> UserScalar:
        """Get user by id"""
        user_dict = await get_user(user_id, info)
        return user_dict

    @strawberry.field
    async def stickynotes(self, info: Info) -> list[StickyNoteScalar]:
        """Get all stickynotes"""
        stickynotes_data_list = await get_stickynotes(info)
        return stickynotes_data_list

    @strawberry.field
    async def stickynote(self, info: Info, stickynote_id: int) -> StickyNoteScalar:
        """Get stickynote by id"""
        stickynote_dict = await get_stickynote(stickynote_id, info)
        return stickynote_dict
