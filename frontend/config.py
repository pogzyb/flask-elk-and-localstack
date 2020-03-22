import os


class Config:
    # Secret encryption salt
    SECRET_KEY=os.getenv('APP_SECRET_KEY')
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('APP_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True