#!/usr/bin/env python3
# -*-coding:utf-8 -*-

from flask_wtf import FlaskForm  # 表单
from wtforms import StringField, SubmitField  # 输入框，提交按钮
from wtforms.validators import DataRequired  # 数据验证


# 定义一个‘名字表单’
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])  # 定义一个输入框
    submit = SubmitField('Submit')  # 定义一个提交按钮
