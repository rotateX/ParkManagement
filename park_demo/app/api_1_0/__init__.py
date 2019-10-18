from flask import Blueprint


api = Blueprint('api', __name__)


from . import views

'''
authentication : api的HTTP登陆验证；
decorators : api的账号权限验证；
errors : 自定义错误信息
views : api视图

'''