import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from app.api.main import router as api_router
from app.graphql.schemas.mutation_schema import Mutation
from app.graphql.schemas.query_schema import Query
from app.graphql.schemas.subscription_schema import Subscription

schema = strawberry.Schema(
    query=Query, mutation=Mutation, subscription=Subscription, config=StrawberryConfig(auto_camel_case=True)
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010)
