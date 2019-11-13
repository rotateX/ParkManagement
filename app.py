# -*- coding : utf-8 -*-

from flask import Flask, url_for, render_template, redirect, request
import config
from parksys.views import parksys
from parkapi.views import parkapi

from exts import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from parksys.models import *



app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
# 导入配置
app.config.from_object('config.ProductionConfig')
# app.config.from_object(config.DevelopmentConfig)

# 注册app
app.register_blueprint(parksys)
app.register_blueprint(parkapi)


# manager = Manager(app)
# Migrate(app, db)
# manager.add_command('db', MigrateCommand)

db.init_app(app)


@app.route('/')
def hello_world():

    # return render_template('parksys/base.html')
    return redirect(url_for('parksys.indexpage'))

if __name__ == '__main__':
    app.run()
    #manager.run()

