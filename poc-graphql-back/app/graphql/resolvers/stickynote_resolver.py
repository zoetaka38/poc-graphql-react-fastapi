from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.orm import load_only

from app.graphql.db.session import get_session
from app.graphql.helpers.helper import get_only_selected_fields, get_valid_data
from app.graphql.models import StickyNote, User
from app.graphql.scalars.stickynotes_scalar import (
    StickyNoteDeleted,
    StickyNoteNotFound,
    StickyNoteScalar,
)
from app.graphql.scalars.user_scalar import UserNotFound


async def get_stickynotes(info):
    """Get all stickynotes resolver"""
    selected_fields = get_only_selected_fields(StickyNote, info)
    async with get_session() as s:
        sql = (
            select(StickyNote)
            .options(load_only(*[getattr(StickyNote, attr) for attr in selected_fields]))
            .order_by(StickyNote.id)
        )
        db_stickynotes = (await s.execute(sql)).scalars().unique().all()

    stickynotes_data_list = []
    for sticky_note in db_stickynotes:
        sticky_note_dict = get_valid_data(sticky_note, StickyNote)
        stickynotes_data_list.append(StickyNoteScalar(**sticky_note_dict))

    return stickynotes_data_list


async def get_stickynote(stickynote_id, info):
    """Get specific stickynote by id resolver"""
    selected_fields = get_only_selected_fields(StickyNote, info)
    async with get_session() as s:
        sql = (
            select(StickyNote)
            .options(load_only(*[getattr(StickyNote, attr) for attr in selected_fields]))
            .filter(id == stickynote_id)
            .order_by(id)
        )
        db_stickynote = (await s.execute(sql)).scalars().unique().one()

    sticky_note_dict = get_valid_data(db_stickynote, StickyNote)
    return StickyNoteScalar(**sticky_note_dict)


async def add_stickynotes(text, user_id):
    """Add stickynotes resolver"""
    async with get_session() as s:
        db_user = None
        sql = select(User).where(User.id == user_id)
        db_user = (await s.execute(sql)).scalars().first()
        if not db_user:
            return UserNotFound()

        db_stickynotes = StickyNote(text=text, created_datetime=datetime.now(), user_id=db_user.id)
        s.add(db_stickynotes)
        await s.commit()

    db_stickynotes_serialize_data = db_stickynotes.as_dict()
    return StickyNoteScalar(**db_stickynotes_serialize_data)


async def delete_stickynotes(stickynote_id):
    """Delete stickynotes resolver"""
    async with get_session() as s:
        sql = select(StickyNote).where(id == stickynote_id)
        existing_db_stickynote = (await s.execute(sql)).first()
        if existing_db_stickynote is None:
            return StickyNoteNotFound()

        query = delete(StickyNote).where(id == stickynote_id)
        await s.execute(query)
        await s.commit()

    return StickyNoteDeleted()


async def update_stickynotes(stickynote_id, text):
    """Update stickynotes resolver"""
    async with get_session() as s:
        sql = select(StickyNote).where(id == stickynote_id)
        existing_db_stickynote = (await s.execute(sql)).first()
        if existing_db_stickynote is None:
            return StickyNoteNotFound()

        query = update(StickyNote).where(id == stickynote_id).values(text=text)
        await s.execute(query)

        sql = select(StickyNote).where(id == stickynote_id)
        db_stickynote = (await s.execute(sql)).scalars().unique().one()
        await s.commit()

    db_stickynotes_serialize_data = db_stickynote.as_dict()
    return StickyNoteScalar(**db_stickynotes_serialize_data)
