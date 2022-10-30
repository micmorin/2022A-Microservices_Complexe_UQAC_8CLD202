from flask_login.login_manager import LoginManager
from models import User

login_manager = LoginManager()

def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'main.main_login'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.get(user_id)
    return None
