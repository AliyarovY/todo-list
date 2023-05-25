from werkzeug.security import generate_password_hash

from backend.base.services import CRUDServiceMixin
from backend.database import get_session
from backend.tables import User
from backend.user.schemas import UserReadSchema, UserCreateSchema


def get_user_by_email(email: str) -> bool:
    session = next(get_session())
    user = (
        session.query(User)
        .filter(
            User.email == email
        )
        .first()
    )
    if not user:
        return False
    return  user


def get_user(id: int):
    session = next(get_session())
    user = (
        session
        .query(User)
        .filter(User.id == id)
        .first()
    )
    if not user:
        return
    return user


def get_user_read_schema(id: int):
    user = get_user(id)
    return UserReadSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        is_superuser=user.is_superuser,
        status=user.status
    )


class UserCRUDService(CRUDServiceMixin):
    table = User

    @classmethod
    def create(cls, **data):
        valid_data = UserCreateSchema(**data).dict()
        password = valid_data.pop('password')
        password_hash = generate_password_hash(password)
        valid_data['password_hash'] = password_hash

        new_user = super().create(**valid_data)
        valid_data['id'] = new_user.id
        return valid_data
