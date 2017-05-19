#!/usr/bin/env python3
#-*-coding:utf-8 -*-
__author__ = 'HZC'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello World!</h1>'
if __name__ == '__main__':
	app.run(debug=True)