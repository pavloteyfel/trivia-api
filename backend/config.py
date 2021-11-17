import os

SECRET_KEY = os.urandom(32)

# Enable debug mode
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/trivia'

# Tracking modifications of objects and emit signals
SQLALCHEMY_TRACK_MODIFICATIONS = False
