#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE_URI = 'sqlite:////path_2_your_db'
DATABASE_URI = 'postgres://username:password@localhost'


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'your_secret_key'

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
