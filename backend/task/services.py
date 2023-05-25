import json

import flask_login
from flask import session

from backend.base.services import CRUDServiceMixin
from backend.tables import Task
from backend.task.schemas import (
    TaskReadSchema,
    TaskCreateSchema,
    TaskUpdateSchema,
)
from backend.user.services import get_user_read_schema, get_user_by_email


class TaskCRUDService(CRUDServiceMixin):
    table = Task

    @classmethod
    def get_query(cls):
        return super().get_query().filter(
            Task.user_id == json.loads(session['user'])['id']
        )

    @classmethod
    def retrieve(cls, id: int):
        task = super().get_object_by_id(id)
        user_schema = get_user_read_schema(task.user_id)
        return TaskReadSchema(
            id=task.id,
            name=task.name,
            description=task.description,
            user=user_schema
        )

    @classmethod
    def list(cls, page: int = 0):
        return [
            cls.retrieve(task.id)
            for task in
            cls.get_query()
        ]

    @classmethod
    def create(cls, **data):
        valid_data = TaskCreateSchema(**data).dict()
        task_id = super().create(**valid_data).id
        return cls.retrieve(task_id)

    @classmethod
    def update(cls, id: int, **data):
        valid_data = TaskUpdateSchema(**data).dict()
        task_id = super().update(id, **valid_data).id
        return cls.retrieve(task_id)

    @classmethod
    def delete(cls, id: int):
        deleted_object = super().delete(id)
        user = get_user_read_schema(deleted_object.user_id)
        return TaskReadSchema(
            id=deleted_object.id,
            name=deleted_object.name,
            description=deleted_object.description,
            user=user,
        )
