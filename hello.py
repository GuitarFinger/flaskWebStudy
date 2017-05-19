#!/usr/bin/env python3
#-*-coding:utf-8 -*-
__author__ = 'HZC'
from flask import Flask
app = Flask(__name__)

#拦截路由
@app.route('/')
def index():
	return '<h1>Hello World!</h1>'
@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, %s</h1>' % name
# 确保直接执行这个脚本时才启动开发Web服务器
if __name__ == '__main__':
	app.run(debug=True) #启动调试模式设置debug为True