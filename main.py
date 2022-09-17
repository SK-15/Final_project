from flask import Flask
import os
from applications import config
from applications.database import db
from applications.model import User, Tracker, Logs
from applications.config import LocalDevelopmentConfig
from applications.rest_api import *
from flask_restful import Api

# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,template_folder="templates")
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
app.app_context().push()
api = Api(app)
app.app_context().push()  

from applications.controller import *

from applications.rest_api import UserAPI
api.add_resource(UserAPI, "/api/user")

from applications.rest_api import TrackerAPI
api.add_resource(TrackerAPI, "/api/tracker/<string:id>")

from applications.rest_api import LogsAPI
api.add_resource(LogsAPI, "/api/logs/<string:id>")

if __name__ == '__main__':
    app.debug = True
    app.run()