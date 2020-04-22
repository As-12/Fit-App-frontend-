"""
main.py

This is an entry point to application
"""

import logging

import os
from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from flask_restx import Api

############################
# App Configuration
############################
from auth.auth import requires_auth, AuthError, requires_auth_with_same_user

app = Flask(__name__)

VERSION = 1.0
API_PREFIX = "/api/v1"
logger = logging.getLogger('fit_application')

# Configuration Files
if os.environ['ENV'] == 'prod':
    app.config.from_pyfile(os.path.join('.', 'conf/api.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.INFO
    logger.level = logging.INFO
elif os.environ['ENV'] == 'dev':
    app.config.from_pyfile(os.path.join('.', 'conf/api.dev.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
    logger.level = logging.DEBUG
elif os.environ['ENV'] == 'test':
    # This is for running test
    app.config.from_pyfile(os.path.join('.', 'conf/api.test.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
    logger.level = logging.DEBUG
else:
    app.config.from_pyfile(os.path.join('.', 'conf/api.local.conf'), silent=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
    logger.level = logging.DEBUG

# Initialize logger
logging.basicConfig()

# Database Configuration
db = SQLAlchemy()
db.app = app
db.init_app(app)

# Load all db database
from database import *

# setup flask-RESTX
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

api = Api(app, version=VERSION, title="Fit-App API", description="Backend API for Fit-App SPA", security='Bearer Auth',
          authorizations=authorizations, prefix=API_PREFIX)

# CORS Configuration
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


# Health-check
@app.route(f"{API_PREFIX}/health")
@cross_origin()
def health_check():
    logger.info(f"Health check triggered from {request.remote_addr}")
    return jsonify( {
        "message": "The App is running",
        "success": True
    }), 200

# import all controllers
from controllers import *


# Handling common error

@app.errorhandler(422)
def unprocessable(error="request cannot be processed"):
    return jsonify({
        "success": False,
        "error": 422,
        "message": str(error)
    }), 422


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run()
