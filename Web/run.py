from flask import Flask
from flask_bootstrap import Bootstrap
from blueprints import main, user, profil, simulator, object, analytics
from login_init import login_manager

if __name__ == "__main__":

    #Initialisation of application
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    login_manager.init_app(app)
    Bootstrap(app)

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(profil)
    app.register_blueprint(simulator)
    app.register_blueprint(object)
    app.register_blueprint(analytics)

    # Start Server
    app.run(host='0.0.0.0',port=80)