#!/usr/bin/env bash

# Running the application
# This should only be used to start local development environment
export ENV=local
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
