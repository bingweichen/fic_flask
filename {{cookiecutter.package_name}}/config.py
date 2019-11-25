#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE_URI = 'sqlite:////Users/chen/myPoject/friends/friends_backend/app.db'
DATABASE_URI = 'postgres://chen@localhost'


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'd*eds-223-ssas-#$dw3-@hdde'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or DATABASE_URI


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
