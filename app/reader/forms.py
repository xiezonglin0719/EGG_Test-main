# -*— coding:utf-8 -*—
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField,PasswordField,IntegerField,TextAreaField,FloatField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo
from wtforms import ValidationError

from app.main.views import read_user_data
# from app.models import User,Book,Library,choices


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        user_data = read_user_data()
        if field.data in user_data:
            raise ValidationError('用户名已存在')

class AddBookForm(FlaskForm):
    book_id = StringField('Book_id',validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    press = StringField('Press', validators=[DataRequired()])
    # choices = choices
    # category = SelectField('Category', validators=[DataRequired()],choices=choices,coerce=str,default=0)
    location = StringField('Location', validators=[DataRequired()])
    brefintro = TextAreaField('Brefintro', validators=[DataRequired()])
    cover = StringField('Avata', validators=[])
    submit = SubmitField('提交')

    flag = 0

class EditBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    press = StringField('Press', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    brefintro = TextAreaField('Brefintro', validators=[DataRequired()])
    submit = SubmitField('提交')


class SearchBookForm(FlaskForm):
    choices = [('1','书名'),('2','作者'),('3','ISBN')]
    option = SelectField('Option',validators=[DataRequired()],choices=choices,coerce=str)
    key = StringField('key',validators=[DataRequired()])
    submit = SubmitField('提交')

class SearchUserForm(FlaskForm):
    choices = [('1','姓名'),('2','联系方式'),('3','证件号')]
    option = SelectField('Option',validators=[DataRequired()],choices=choices,coerce=str)
    key = StringField('key',validators=[DataRequired()])
    submit = SubmitField('提交')

class AdminUserForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    gender = StringField('Gender', validators=[])
    id = StringField('Id', validators=[])
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField('确认修改')

class AdminPasswdForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('确认修改')


class SysSetForm(FlaskForm):
    maxuser = StringField('Maxuser', validators=[DataRequired()])
    maxbook = StringField('Maxbook', validators=[DataRequired()])
    maxtime = StringField('Maxtime', validators=[DataRequired()])
    submit = SubmitField('确认修改')


class WantEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    press = StringField('Press', validators=[DataRequired()])
    # choices = choices
    # category = SelectField('Category', validators=[DataRequired()], choices=choices, coerce=str, default=0)
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('提交')
