from typing import Any
from backend.database import get_session


class CRUDServiceMixin:
    table = ...
    session = next(get_session())
    pagination: int = 100

    @classmethod
    def get_query(cls):
        return cls.session.query(cls.table)

    @classmethod
    def get_id_field(cls):
        return cls.table.id

    @classmethod
    def get_object_by_id(cls, id: Any):
        res = (
            cls.get_query()
            .filter(
                cls.get_id_field() == id
            )
            .first()
        )
        return res

    @classmethod
    def create(cls, **data):
        res = cls.table(**data)
        cls.session.add(res)
        cls.session.commit()
        return res

    @classmethod
    def retrieve(cls, id: Any):
        return cls.get_object_by_id(id)

    @classmethod
    def list(cls, page: int = 0):
        if page < 0:
            page = 0
        return (
            cls.get_query()
            .offset(page * cls.pagination)
            .limit(cls.pagination)
            .all()
        )

    @classmethod
    def update(cls, id: Any, **data):
        res = cls.get_object_by_id(id)
        for k, v in data.items():
            setattr(cls.table, k, v)
        cls.session.commit()

        return res

    @classmethod
    def delete(cls, id: Any):
        res = cls.get_object_by_id(id)
        cls.session.delete(res)
        cls.session.commit()

        return res
