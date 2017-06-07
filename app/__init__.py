#!/usr/bin/env python3
# -*-coding:utf-8 -*-

from flask import Flask  # flask模块
from flask_bootstrap import Bootstrap  # bootstrap模块
from flask_mail import Mail  # 邮箱模块
from flask_moment import Moment  # 时间模块
from flask_sqlalchemy import SQLAlchemy  # 数据库模块
from config import config  # 自定义配置模块

# 实例
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app