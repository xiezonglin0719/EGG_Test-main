# -*— coding:utf-8 -*—
import os

from flask_script import Manager

from app import create_app
from app.reader import reader


app = create_app('default')
app.register_blueprint(reader)
manager = Manager(app)
# 移除与数据库迁移和管理相关的代码
# from flask_migrate import Migrate
# from flask_script import Manager
# migrate = Migrate(app, db)
# manager = Manager(app)

# 移除数据库相关的 shell 上下文处理器
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Book=Book)

#启动onlinedisplay模块
if __name__ == '__main__':
    from onlinedisplay import start_onlinedisplay
    import threading
    # 开启一个线程运行 WebSocket 服务
    t = threading.Thread(target=start_onlinedisplay)
    t.start()

    # 运行 Flask 应用
    app.run()