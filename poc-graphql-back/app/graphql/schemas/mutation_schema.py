import strawberry
from strawberry.types import Info

from app.graphql.db.redis import get_redis
from app.graphql.fragments.stickynotes_fragments import (
    AddStickyNotesResponse,
    DeleteStickyNotesResponse,
    UpdateStickyNotesResponse,
)
from app.graphql.fragments.user_fragments import AddUserResponse, DeleteUserResponse
from app.graphql.inputs.user_input import UserInput
from app.graphql.resolvers.stickynote_resolver import (
    add_stickynotes,
    delete_stickynotes,
    update_stickynotes,
)
from app.graphql.resolvers.user_resolver import add_user, delete_user
from app.graphql.schemas.subscription_schema import stickynote_subscriptions


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def add_stickynotes(self, text: str, user_id: int, info: Info) -> AddStickyNotesResponse:
        """Add sticky note"""
        async for redis_client in get_redis():
            add_stickynotes_resp = await add_stickynotes(text, user_id)
            await stickynote_subscriptions.publish(add_stickynotes_resp, redis_client)
            return add_stickynotes_resp

    @strawberry.mutation
    async def add_user(self, user: UserInput) -> AddUserResponse:
        """Add user"""
        add_user_resp = await add_user(user.name)
        return add_user_resp

    @strawberry.mutation
    async def delete_user(self, user: UserInput) -> DeleteUserResponse:
        """Delete user"""
        delete_user_resp = await delete_user(user_id=user.id)
        return delete_user_resp

    @strawberry.mutation
    async def delete_stickynote(self, stickynote_id: int) -> DeleteStickyNotesResponse:
        """Delete Sticky Notes"""
        delete_stickynote_resp = await delete_stickynotes(stickynote_id)
        return delete_stickynote_resp

    @strawberry.mutation
    async def update_stickynote(self, stickynote_id: int, text: str) -> UpdateStickyNotesResponse:
        """Update Sticky Notes"""
        update_stickynote_resp = await update_stickynotes(stickynote_id, text)
        return update_stickynote_resp
