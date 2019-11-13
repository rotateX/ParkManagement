# -*- coding : utf-8 -*-

from app import app
from exts import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from parksys.models import *

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ =='__main__':
    manager.run()
