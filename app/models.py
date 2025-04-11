
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 模拟数据库存储的字典
users = {}
books = {}
librarys = {}
requests = {}
wants = {}
sysinfo = {}
statics = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash=None, name=None, gender=1, depart=None, post=None, contact=None, room=None, user_type=1, avata='lost'):
        self.id = id
        self.username = username
        # self.password_hash = password_hash
        # self.name = name
        # self.gender = gender
        # self.depart = depart
        # self.post = post
        # self.contact = contact
        # self.room = room
        # self.user_type = user_type
        # self.avata = avata
        # self.own_books = []  # 模拟反向关联

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
# app/models.py
def load_user(user_id):
    # 假设用户信息存储在 user_data.json 中
    import json
    try:
        with open('user_data.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
            for user_info in users:
                if isinstance(user_info, dict) and str(user_info.get('id')) == str(user_id):
                    from app.models import User  # 假设 User 类在 app.models 中定义
                    print(user_info)
                    return User(user_info.get('id'), user_info.get('username'))
    except FileNotFoundError:
        return None
    return None
