#!/usr/bin/env python3
# -*-coding:utf-8 -*-
__author__ = 'HZC'
from flask import Flask, render_template, session, redirect, url_for  # 渲染模板模块render_template
from flask_script import Manager  # 为flask程序添加了一个命令行解析器
from flask_bootstrap import Bootstrap  # 导入bootstrap框架
from flask_moment import Moment  # 本地化日期和时间
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)  # 程序实例是Flask类的对象，把接收自客户端的所有请求都交给这个对象处理
app.config['SECRET_KEY'] = 'hard to guess string'  # 设置密钥

manager = Manager(app)  # manager实例
bootstrap = Bootstrap(app)  # bookstrap实例
moment = Moment(app)


# -------------------拦截路由---------------------

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
        session['name'] = form.name.data  # 将姓名存在session里面
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    manager.run()
