# -*— coding:utf-8 -*—
import os
from socket import SocketIO


from app import create_app, db
from flask_migrate import Migrate
from flask_script import Manager
from app.models import User, Book
from app.reader import reader

app = create_app('default')
app.register_blueprint(reader)
migrate = Migrate(app, db)

manager = Manager(app)


# 建表，删除表，首次部署时执行（调试过程中不要执行，否则数据将全部删除）
# db.drop_all()
# db.create_all()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book)


# if __name__ == '__main__':
#      app.run()
#启动onlinedisplay模块
if __name__ == '__main__':
    from onlinedisplay import start_onlinedisplay
    import threading

    # 开启一个线程运行 WebSocket 服务
    t = threading.Thread(target=start_onlinedisplay)
    t.start()

    # 运行 Flask 应用
    app.run()

