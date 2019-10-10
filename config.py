# -*- coding : utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

per_page = 10
class Config:
    '''
    基础配置
    '''
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'park'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://parkuser:park2019@127.0.0.1:3306/myflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

class ProductionConfig(Config):
    '''
    正式生产环境
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'propark'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://parkuser:park2019@127.0.0.1:3306/myflask'


class DevelopmentConfig(Config):
    '''
    开发环境配置
    '''
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devpark'