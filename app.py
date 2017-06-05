#!/usr/bin/env python3
# -*-coding:utf-8 -*-
__author__ = 'HZC'
# 渲染模板模块render_template
# session 用户会话，是请求上下文中的变量
# redirect 重定向，参数是重定向的URL
# url_for URL生成函数,第一个参数是端点名，是相应视图函数的名字
# flash 提示消息 使用get_flashed_messages() 函数开放给模板,用来获取并渲染消息
import os  # 操作系统模块
from threading import Thread  # 引入线程
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell  # 为flask程序添加了一个命令行解析器
from flask_bootstrap import Bootstrap  # 导入bootstrap框架
from flask_moment import Moment  # 本地化日期和时间
from flask_wtf import FlaskForm  # 表单
from wtforms import StringField, SubmitField  # 表单输入框和提交按钮
from wtforms.validators import DataRequired  # 表单校验 数据校验
from flask_sqlalchemy import SQLAlchemy  # 数据库
from flask_migrate import Migrate, MigrateCommand  # 数据库迁移
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))  # 返回脚本的路径

app = Flask(__name__)  # 程序实例是Flask类的对象，把接收自客户端的所有请求都交给这个对象处理
app.config['SECRET_KEY'] = 'hard to guess string'  # 设置密钥
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')  # 保存数据库url
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后都会自动提交数据库中得变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 传输邮箱
app.config['MAIL_PORT'] = 587  # 端口号
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # 邮箱 配置在系统环境变量中
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # 密码 配置在系统环境变量中
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '815547360@qq.com'
app.config['FLASKY_ADMIN'] = '815547360@qq.com'

# 实例对象
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


# ----------------------类-----------------------
class Role(db.Model):
    __tablename__ = 'roles'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 列
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):  # 自动调用函数 返回一个对象
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 外键

    def __repr__(self):
        return '<User %r>' % self.username


# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():  # 注册上下文
        mail.send(msg)


# 参数： 收件人地址、主题、渲染邮件正文的模板、关键字参数列表
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 把对象添加到导入列表中，为shell命令注册一个make_context回调函数
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))  # 定制shell
manager.add_command('db', MigrateCommand)


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
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                print('hello')
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

if __name__ == '__main__':
    db.create_all()
    manager.run()
