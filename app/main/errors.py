# -*— coding:utf-8 -*—
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_no_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500