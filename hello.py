#!/usr/bin/env python3
# -*-coding:utf-8 -*-
__author__ = 'HZC'
from flask import Flask
from flask_script import Manager  # 为flask程序添加了一个命令行解析器

app = Flask(__name__)  # 程序实例是Flask类的对象，把接收自客户端的所有请求都交给这个对象处理

manager = Manager(app)


# 拦截路由
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


# 动态路由
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s</h1>' % name


if __name__ == '__main__':
    manager.run()
