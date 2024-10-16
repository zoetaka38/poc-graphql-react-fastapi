import json
from dataclasses import dataclass, fields
from datetime import datetime
from typing import AsyncGenerator, Optional

import strawberry
from strawberry.types import Info

from app.graphql.brokers.stickynote_broker import StickyNoteSubscriptionBroker
from app.graphql.db.redis import get_redis
from app.graphql.scalars.stickynotes_scalar import StickyNoteScalar


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def subscribe_stickynote(self, info: Info) -> AsyncGenerator[Optional[StickyNoteScalar], None]:
        async for redis_client in get_redis():
            async for message in stickynote_subscriptions.subscribe(redis_client):
                data = json.loads(message["data"])
                key_type_list = [{"key": field.name, "type": field.type} for field in fields(StickyNoteScalar)]
                for key_type in key_type_list:
                    if key_type["type"] == datetime or key_type["type"] == datetime | None:
                        data[key_type["key"]] = datetime.fromisoformat(data[key_type["key"]])
                stickynote = StickyNoteScalar(**data)
                yield stickynote


stickynote_subscriptions = StickyNoteSubscriptionBroker()
