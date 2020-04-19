"""
main.py

This is an entry point to application
"""

import logging

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from flask_restx import  Api


############################
# App Configuration
############################
app = Flask(__name__)


VERSION = 1.0


# Configuration Files
if os.environ['ENV'] == 'prod':
    app.config.from_pyfile(os.path.join('.', 'conf/api.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.INFO
elif os.environ['ENV'] == 'dev':
    app.config.from_pyfile(os.path.join('.', 'conf/api.dev.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
elif os.environ['ENV'] == 'test':
    # This is for running test
    app.config.from_pyfile(os.path.join('.', 'conf/api.test.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
else:
    app.config.from_pyfile(os.path.join('.', 'conf/api.local.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG


# Database Configuration
db = SQLAlchemy()
db.app = app
db.init_app(app)


# Load all db database
from database import *



# Db initializations
db.drop_all()
db.create_all()


# setup flask-RESTX
api = Api(app, version=VERSION, title="Fit-App API", description="Backend API for Fit-App SPA")


# CORS Configuration
CORS(app)


# CORS(app, resources={r"*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


# Health-check
# @TODO: Secure this route so only admin can run this
@app.route("/health")
@cross_origin()
def health_check():
    return "Fit-App API is running"


# import all controllers
from controllers import *

if __name__ == '__main__':
    app.run()
