#!/usr/bin/env python3
# -*-coding:utf-8 -*-

from threading import Thread  # 多线程处理
from flask import current_app, render_template  # 当前激活程序实例, 跳转
from flask_mail import Message  # 邮箱消息
from . import mail  # 邮箱


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr