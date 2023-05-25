import flask
import flask_login
from flask_swagger_ui import get_swaggerui_blueprint

from backend.config import settings
from backend.task.routes import task_blueprint
from backend.user.routes import user_blueprint
from backend.user.services import get_user_by_email
from backend.user.user_login import UserLogin

app = flask.Flask(__name__)

app.secret_key = settings.secret_key

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

SWAGGER_URL = '/api/docs'
API_URL = 'http://petstore.swagger.io/v2/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={
        'app_name': "TODO List API"
    },

)

app.register_blueprint(swaggerui_blueprint)


@login_manager.user_loader
def user_loader(email):
    if not get_user_by_email(email):
        return

    user = UserLogin()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not get_user_by_email(email):
        return

    user = UserLogin()
    user.id = email
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == '__main__':
    app.register_blueprint(task_blueprint, url_prefix='/task')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    app.run(
        host=settings.server_host,
        port=settings.server_port,
        debug=settings.debug,
    )
