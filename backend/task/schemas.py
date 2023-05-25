from pydantic import BaseModel

from backend.user.schemas import UserReadSchema


class TaskBaseSchema(BaseModel):
    name: str


class TaskReadSchema(TaskBaseSchema):
    id: int
    description: str | None
    user: UserReadSchema


class TaskCreateSchema(TaskBaseSchema):
    description: str | None = None
    user_id: int


class TaskUpdateSchema(TaskBaseSchema):
    description: str
    user_id: int
