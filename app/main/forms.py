# -*— coding:utf-8 -*—
import json

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField,PasswordField,IntegerField,TextAreaField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo
from wtforms import ValidationError

#
# from app.models import User,Book,Library,choices

# 假设 user_data.json 文件存储在项目根目录下
USER_DATA_FILE = 'user_data.json'

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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('注册')


def validate_username(self, field):
        user_data = read_user_data()
        if field.data in user_data:
            raise ValidationError('用户名已存在')
