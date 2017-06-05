#!/usr/bin/env python3
# -*-coding:utf-8 -*-
__author__ = 'HZC'
# 渲染模板模块render_template
# session 用户会话，是请求上下文中的变量
# redirect 重定向，参数是重定向的URL
# url_for URL生成函数,第一个参数是端点名，是相应视图函数的名字
# flash 提示消息 使用get_flashed_messages() 函数开放给模板,用来获取并渲染消息
import os  # 操作系统模块
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager  # 为flask程序添加了一个命令行解析器
from flask_bootstrap import Bootstrap  # 导入bootstrap框架
from flask_moment import Moment  # 本地化日期和时间
from flask_wtf import FlaskForm  # 表单
from wtforms import StringField, SubmitField  # 表单输入框和提交按钮
from wtforms.validators import DataRequired  # 表单校验 数据校验
from flask_sqlalchemy import SQLAlchemy  # 数据库

basedir = os.path.abspath(os.path.dirname(__file__))  # 返回脚本的路径

app = Flask(__name__)  # 程序实例是Flask类的对象，把接收自客户端的所有请求都交给这个对象处理
app.config['SECRET_KEY'] = 'hard to guess string'  # 设置密钥
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')  # 保存数据库url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后都会自动提交数据库中得变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 实例对象
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


# ----------------------类-----------------------
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# -------------------拦截路由---------------------
# 404页面:客户端请求位置页面或路由时显示
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500页面:有未处理的异常时显示
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')  # 提示消息
        session['name'] = form.name.data  # 将姓名存在session里面
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    db.create_all()
    manager.run()
