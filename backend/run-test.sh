#!/usr/bin/env bash

# Unit Testing the application
# This should only be used to start local development environment
export ENV=test
python -m unittest test_fitapp.py
