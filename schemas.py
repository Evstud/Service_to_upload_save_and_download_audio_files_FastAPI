from pydantic import BaseModel
from uuid import UUID


class BaseUser(BaseModel):
    user_name: str


class SaveAudio(BaseModel):
    user_id: UUID
    user_token: UUID
