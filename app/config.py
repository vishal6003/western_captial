import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'  # Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'  # Secret key for sessions
