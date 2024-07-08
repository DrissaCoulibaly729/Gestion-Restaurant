import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1TontonC@localhost/restaurant_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key
    SECRET_KEY = 'you-will-never-guess'
    
    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'dc377303@gmail.com'
    MAIL_PASSWORD = 'glyl azpi agst kcqb'
    MAIL_DEFAULT_SENDER = 'dc377303@gmail.com'
