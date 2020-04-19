#!/usr/bin/env bash

# Running the application
# This should only be used to start local development environment
export ENV=local
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
