from os import environ


class Config(object):
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "9OLWxND4o83j4K4iuopO"
    SEND_FILE_MAX_AGE_DEFAULT = 0
    DEBUG = True
