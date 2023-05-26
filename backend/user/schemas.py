from enum import Enum

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    username: str
    is_superuser: bool = False


class UserCreateSchema(UserBaseSchema):
    password: str


class UserReadSchema(UserBaseSchema):
    id: int


class UserSchema(UserReadSchema):
    password_hash: str

    class Config:
        orm_mode = True
