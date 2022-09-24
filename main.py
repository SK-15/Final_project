from flask import Flask
# import os
# from applications import config
from applications.database import db
# from applications.model import User, Tracker, Logs
from applications.config import LocalDevelopmentConfig
from applications.rest_api import *
from flask_restful import Api

# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
api.init_app(app)
app.app_context().push()  

from applications.controller import *

if __name__ == '__main__':
    app.debug = True
    app.run()