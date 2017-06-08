#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import os  # 系统模块
from app import create_app, db  # 当前激活程序的程序实例
from app.models import User, Role  # 导入模块
from flask_script import Manager, Shell  # 脚本运行管理, 命令行
from flask_migrate import Migrate, MigrateCommand  # 数据迁移

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
