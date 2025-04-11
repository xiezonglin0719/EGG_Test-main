# -*— coding:utf-8 -*—
import os
import sys

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import config
from app.models import load_user  # 导入 load_user 函数


bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message = '请先登录'
login_manager.login_view = '/login'


def create_app(config_name):
    if hasattr(sys, '_MEIPASS'):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
    else:
        template_folder = os.path.join(os.getcwd(), 'app/templates')

    # template_folder = os.path.join(os.getcwd(), 'app/templates')
    print(f"模板文件夹路径: {template_folder}")
    app = Flask(__name__, template_folder=template_folder)
    # 调用配置类中初始化函数，初始化app，这里该初始化函数为空
    secret_key = "dqwiojdwoi123"
    if secret_key is None:
        print("SECRET_KEY environment variable is not set!")
    else:
        app.config['SECRET_KEY'] = secret_key
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    # 初始化用到的各个模块（关联到当前app）
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # 添加 user_loader 回调函数
    @login_manager.user_loader
    def load_user_callback(user_id):
        return load_user(user_id)

    # 注册蓝图(导入包初始化模块__init__中的内容时，需要加‘.’)
    from .main import main as main_bp
    from .reader import reader as reader_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(reader_bp, url_prefix='/reader')
    # 返回 flask 实例
    return app