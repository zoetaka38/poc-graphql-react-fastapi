import asyncio
import dataclasses
import json
from datetime import datetime
from typing import AsyncGenerator, Optional

import redis.asyncio as redis
import strawberry
from strawberry.types import Info

from app.graphql.db.redis import get_redis
from app.graphql.resolvers.stickynote_resolver import get_stickynote, get_stickynotes
from app.graphql.scalars.stickynotes_scalar import StickyNoteScalar


class StickyNoteSubscriptionBroker:
    channel = "channel:StickyNote"

    async def publish(self, stickynote: StickyNoteScalar, redis: redis.Redis):
        def datetime_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        payload = json.dumps(dataclasses.asdict(stickynote), default=datetime_serializer)
        await redis.publish(self.channel, payload)

    async def subscribe(self, redis: redis.Redis) -> dict:  # type: ignore
        pubsub = redis.pubsub()
        await pubsub.subscribe(self.channel)
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            yield message
