#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: __init__.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-05-20 12:35:52 (CST)
# Last Update:星期一 2016-7-25 11:11:52 (CST)
#          By:jianglin
# Description:
# **************************************************************************
from flask import Flask, g, send_from_directory, request
from maple.extensions import (register_login, register_redis, register_mail,
                              register_cache)
from maple.extensions import (register_form, register_babel,
                              register_principal, register_jinja2,
                              register_avatar, register_maple)
from maple.extensions import register_rbac
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
import os


def create_app():
    templates = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir, 'templates'))
    static = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir, 'static'))

    app = Flask(__name__, template_folder=templates, static_folder=static)
    app.config.from_object('config.config')
    app.url_map._rules.clear()
    app.url_map._rules_by_endpoint.clear()
    app.url_map.default_subdomain = 'forums'
    app.add_url_rule(app.static_url_path + '/<path:filename>',
                     endpoint='static',
                     view_func=app.send_static_file,
                     subdomain='forums')
    return app


def register(app):
    register_avatar(app)
    register_babel(app)
    register_form(app)
    register_principal(app)
    register_jinja2(app)
    register_maple(app)
    register_routes(app)


def register_routes(app):
    from .urls import register_urls
    register_urls(app)


app = create_app()
db = SQLAlchemy(app)
mail = register_mail(app)
login_manager = register_login(app)
redis_data = register_redis(app)
cache = register_cache(app)
rbac = register_rbac(app)
register(app)


@app.before_request
def before_request():
    from maple.forums.forms import SortForm, SearchForm
    g.user = current_user
    g.sort_form = SortForm()
    g.search_form = SearchForm()


@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
