# -*— coding:utf-8 -*—
from flask import render_template, request, session, redirect, url_for, abort, flash, json, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from . import main
from .forms import LoginForm, RegisterForm

from app.models import User
from sqlalchemy import or_, and_
from datetime import datetime

# 读取本地用户信息
def read_user_data():
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# 写入本地用户信息
def write_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# ------------------------------ 渲染页面路由 --------------------------------#
# 浏览器首页
@main.route('/')
def first():
    return redirect(url_for('main.login'))


# 系统首页
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('signal.html')

# 假设 user_data.json 文件存储在项目根目录下
USER_DATA_FILE = 'user_data.json'

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_user_data(users):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# test/main/views.py
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = load_user_data()
        for user_info in users:
            if isinstance(user_info, dict) and user_info.get('username') == form.username.data:
                user = User(user_info.get('id'), user_info.get('username'))
                login_user(user, True)
                return redirect(url_for('function.index'))  # 修改重定向目标
        flash('用户名不存在')
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = load_user_data()
        username = form.username.data
        # 检查用户名是否已存在
        for user in users:
            if user.get('username') == username:
                flash('用户名已存在，请选择其他用户名。')
                return render_template('register.html', form=form)
        # 生成新用户 ID
        new_user_id = len(users) + 1
        new_user = {
            'id': new_user_id,
            'username': username,
        }
        users.append(new_user)
        save_user_data(users)
        flash('注册成功，请登录。')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))

# 图书回收界面，显示图书回收申请列表，操作（回收）
@main.route('/bookmanage/returnbook', methods=['GET', 'POST'])
@login_required
def returnbook():
    return render_template('returnbook.html')


# 读者想看页，显示读者提交的疲劳数据单
@main.route('/wantsmanage/wantsbook', methods=['GET', 'POST'])
@login_required
def wantsbook():
    return render_template('evaluate.html')


# ------------------------------ 数据 api --------------------------------#
# 返回当前登录的用户名，用于动态更新标题栏用户名
@main.route('/api/username', methods=['GET', 'POST'])
@login_required
def username_api():
    return jsonify({'username': current_user.username})

# 从数据库中获取用户头像链接(不区分管理员普通用户)
@main.route('/api/get_avata_url', methods=['GET', 'POST'])
def get_avata_url_api():
    username = request.get_data().decode().split('=')[1]
    user = User.query.filter_by(username=username).first()
    result = {"url": user.avata}
    return jsonify(result)

