from flask import Flask
from blueprints import main, data

if __name__ == "__main__":

    #Initialisation of application
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    app.register_blueprint(main)
    app.register_blueprint(data)
    
    # Start Server
    app.run(host='0.0.0.0',port=5000)