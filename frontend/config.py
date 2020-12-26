import os


class Config:
    # Secret encryption salt
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('APP_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Cache config
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    # Custom Mail sender
    MAIL_WORKERS = os.getenv('MAIL_WORKERS', 1)


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


def get_config(env: str):
    configs = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.testingConfig',
    }
    return configs.get(env)
