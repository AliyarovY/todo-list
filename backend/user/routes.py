import flask
import flask_login
from flask import Blueprint, request, session
from flask_pydantic import validate
from werkzeug.security import check_password_hash

from backend.user.schemas import UserSchema
from backend.user.user_login import UserLogin
from backend.user.services import UserCRUDService, get_user_by_email

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/registration', methods=['POST'])
@validate()
def registration():
    return UserCRUDService.create(**request.get_json())


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    current_user = get_user_by_email(email)

    session['email'] = email
    session['user'] = UserSchema.from_orm(current_user).json()

    if all((
            not not current_user,
            check_password_hash(current_user.password_hash, flask.request.form['password']),
    )):
        user = UserLogin()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('task.list'))

    return 'Bad login'


@user_blueprint.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@user_blueprint.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'



