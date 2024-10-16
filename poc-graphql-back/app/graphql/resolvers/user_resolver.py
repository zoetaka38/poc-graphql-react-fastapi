from sqlalchemy import delete, insert, select
from sqlalchemy.orm import load_only, subqueryload

from app.graphql.db.session import get_session
from app.graphql.helpers.helper import (
    fetch_data,
    fetch_single_data,
    get_only_selected_fields,
    get_valid_data,
)
from app.graphql.models import User
from app.graphql.scalars.stickynotes_scalar import StickyNoteScalar
from app.graphql.scalars.user_scalar import (
    AddUser,
    UserDeleted,
    UserExists,
    UserNotFound,
    UserScalar,
)

scalar_mapping = {
    "stickynotes": StickyNoteScalar,
    # Add other mappings here if needed
}


async def get_users(info):
    """Get all users resolver"""
    selected_fields = get_only_selected_fields(User, info)
    return await fetch_data(scalar_mapping, selected_fields, User, UserScalar)


async def get_user(user_id, info):
    """Get specific user by id resolver"""
    selected_fields = get_only_selected_fields(User, info)
    return await fetch_single_data(scalar_mapping, selected_fields, User, UserScalar, user_id)


async def add_user(name):
    """Add user resolver"""
    async with get_session() as s:
        sql = select(User).options(load_only(User.name)).filter(User.name == name)
        existing_db_user = (await s.execute(sql)).first()
        if existing_db_user is not None:
            return UserExists()

        query = insert(User).values(name=name)
        await s.execute(query)

        sql = select(User).options(load_only(User.name)).filter(User.name == name)
        db_user = (await s.execute(sql)).scalars().unique().one()
        await s.commit()

    db_user_serialize_data = db_user.as_dict()
    return AddUser(**db_user_serialize_data)


async def delete_user(user_id):
    """Delete user resolver"""
    async with get_session() as s:
        sql = select(User).where(User.id == user_id)
        existing_db_user = (await s.execute(sql)).first()
        if existing_db_user is None:
            return UserNotFound()

        query = delete(User).where(User.id == user_id)
        await s.execute(query)
        await s.commit()

    return UserDeleted()
