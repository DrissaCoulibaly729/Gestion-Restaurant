import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost/Gestion-Restaurant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
