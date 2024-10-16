import strawberry


@strawberry.input
class UserInput:
    id: int | None = None
    name: str
