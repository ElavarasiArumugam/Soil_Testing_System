# backend/config.py
import os

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')
    # Define the path for the SQLite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'database', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False