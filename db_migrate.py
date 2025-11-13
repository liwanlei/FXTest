# @Time    : 2017/7/13 20:54
# @Author  :  lileilei
# @File    : db_migrate.py
'''数据库同步使用'''
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db, app

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
