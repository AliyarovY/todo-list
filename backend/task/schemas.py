from enum import Enum

from pydantic import BaseModel

from backend.user.schemas import UserReadSchema


class Status(Enum):
    new = 'new'
    active = 'active'
    completed = 'completed'


class TaskBaseSchema(BaseModel):
    name: str
    status: Status


class TaskReadSchema(TaskBaseSchema):
    id: int
    description: str | None
    user: UserReadSchema


class TaskCreateSchema(TaskBaseSchema):
    description: str | None = None
    user_id: int


class TaskUpdateSchema(BaseModel):
    status: Status
