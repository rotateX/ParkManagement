# -*- coding : utf-8 -*-

from flask import Flask, url_for, render_template, redirect, request
import config


from flask_login import LoginManager
from exts import db

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
# 导入配置
app.config.from_object('config.ProductionConfig')
# app.config.from_object(config.DevelopmentConfig)

# 注册app
# manager = Manager(app)
# Migrate(app, db)
# manager.add_command('db', MigrateCommand)

db.init_app(app)  # 数据库操作的关联

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'parksys.login'
login_manager.session_protection = "strong"
login_manager.login_message = '请登录以访问此页面'

from parksys.models import *
from parksys.views import parksys
from parkapi.views import parkapi


app.register_blueprint(parksys)
app.register_blueprint(parkapi)


@app.route('/')
def hello_world():
    # return render_template('parksys/base.html')
    return redirect(url_for('parksys.indexpage'))

if __name__ == '__main__':
    app.run()
    #manager.run()

