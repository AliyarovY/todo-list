from flask import Blueprint, request
from flask_login import login_required
from flask_pydantic import validate

from backend.task.services import TaskCRUDService

task_blueprint = Blueprint('task', __name__)


@task_blueprint.route("/<id>", methods=["GET"])
@login_required
@validate()
def read(id):
    return TaskCRUDService.retrieve(id)

@task_blueprint.route("/", methods=["GET"])
@login_required
@validate(response_many=True)
def list():
    page = request.args.to_dict().get('page', 0)
    page = int(page)
    return TaskCRUDService.list(page)


@task_blueprint.route("/", methods=["POST"])
@login_required
@validate()
def create():
    data = request.get_json()
    return TaskCRUDService.create(**data)


@task_blueprint.route("/<id>", methods=["PUT"])
@login_required
@validate()
def update(id):
    data = request.get_json()
    return TaskCRUDService.update(id, **data)


@task_blueprint.route("/<id>", methods=["DELETE"])
@login_required
@validate()
def delete(id):
    return TaskCRUDService.delete(id)
