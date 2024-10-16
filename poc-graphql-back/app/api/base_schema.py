from pydantic import BaseModel as BaseModel_


class BaseModel(BaseModel_):
    class Config:
        extra = "forbid"
