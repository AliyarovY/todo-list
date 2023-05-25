from enum import Enum

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    username: str


class Status(Enum):
    new = 'new'
    active = 'active'
    completed = 'completed'


class UserCreateSchema(UserBaseSchema):
    is_superuser: bool = False
    status: Status = 'new'
    password: str


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool
    status: Status


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    is_superuser: bool
    password_hash: str
    status: Status

    class Config:
        orm_mode = True
