from os import environ


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgres://xvqqlxtesvymrr:b8854a94fdef37b4fd6ede95b997f42ddde12996945a893a004b4415aba175e0@ec2-54-227-249-108.compute-1.amazonaws.com:5432/d76jpvvpi9asaa"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "9OLWxND4o83j4K4iuopO"
    SEND_FILE_MAX_AGE_DEFAULT = 0
    DEBUG = True
