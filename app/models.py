#!/usr/bin/env python3
# -*-coding:utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash  # 生成密码散列， 验证散列值
from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # [id]主键
    username = db.Column(db.String(64), unique=True, index=True)  # [用户名]
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # [外键]
    password_hash = db.Column(db.String(128))  # [密码散列值]

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
