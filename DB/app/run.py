from flask import Flask
from blueprints import main, user, profil, calcul
import database_init

if __name__ == "__main__":

    #Initialisation of application
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    database_init.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(profil)
    app.register_blueprint(calcul)
    
    # Start Server
    app.run(host='0.0.0.0',port=5000)