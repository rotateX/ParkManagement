import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    pass


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass


config = {'default': DevelopmentConfig,
          'development': DevelopmentConfig,
          'production': ProductionConfig,
          'testing': TestingConfig
          }

