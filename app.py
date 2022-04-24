import os
from flask import Flask, session
# from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
# from application import config
from application.config import LocalDevelopmentConfig, HerokuProductionConfig
from application.database import db


app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")

    # app.secret_key = "thisisasecretkey"  #########################___test

    if os.getenv('ENV', default=None) == "heroku_production":
        app.secret_key = os.getenv('SECRET_KEY', default=None) #SECRET_KEY
        print("Starting Heroku Production Mode...")
        app.config.from_object(HerokuProductionConfig)
    elif os.getenv('ENV', default=None) == "local_development":
        app.secret_key = "thisisasecretkey" #SECRET_KEY
        print("Starting Local Development[elif]...")
        app.config.from_object(LocalDevelopmentConfig)
    else:
        app.secret_key = "thisisasecretkey" #SECRET_KEY
        print("Starting Local Development[else]...")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()


# import all the controllers so they are loaded..
from application.controllers import *

# import all the apis so they are loaded..
from application.api import * #TrackerAPI
api.add_resource(TrackerAPI, '/api/tracker', '/api/tracker/<int:tracker_id>')
api.add_resource(AllTrackersAPI, '/api/alltrackers/<int:user_id>')
api.add_resource(UserAPI, '/api/user/<string:username>')


if __name__=="__main__":
    # Run the flask app
    app.run()