#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import os  # 系统模块

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前脚本路径


# 基类Config包含通用配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string.'  # 密钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 将会追踪对象的修改并且发送信号,默认为True
    MAIL_SERVER = 'smtp.qq.com'  # SMTP(简单邮箱传输协议)服务器地址(端口465或587)
    MAIL_PORT = 587  # 端口号
    MAIL_USE_TLS = True  # 启用TLS(Transport Layer Security) 传输层安全,继承SSL(安全套接层),在传输层对网络连接进行加密
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 敏感信息存在于环境变量中获取系统变量MAIL_USERNAME
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 邮件发件标题
    FLASKY_MAIL_SENDER = '815547360@qq.com'  # 发件人邮箱地址
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # 管理员邮箱地址

    # classmethod将方法变成类方法,自动传给方法的第一个参数是类，而不是类的实例
    # staticmethod将class中的方法变成静态方法,可以当作普通方法一样调用,而不会将类实例本身作为第一个self参数传给方法
    @staticmethod
    def init_app(app):  # 在之前创建的扩展对象上调用init_app()可以完成初始化过程
        pass  # 占位语句,是为了保持程序结构的完整性


# 子类 分类定义专用的配置
class DevelopmentConfig(Config):
    DEBUG = True  # 调试模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')  # 保存数据库URL


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
