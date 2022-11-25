from flask_login.login_manager import LoginManager
from models import User
from flask import redirect, url_for, request

login_manager = LoginManager()

def init_app(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('main.main_login', next=request.path))