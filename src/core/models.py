from pydantic import BaseModel


class Model(BaseModel):
    identifier: int
    version: int