# -*— coding:utf-8 -*—
import threading
import time
from random import random
from socket import SocketIO
import random
import joblib
import numpy as np
import socketio
from flask import render_template, request, session, redirect, url_for, abort, flash, json, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from . import reader
from .forms import LoginForm, RegisterForm, AddBookForm, EditBookForm, SearchBookForm, \
    SearchUserForm, AdminUserForm, AdminPasswdForm, SysSetForm, WantEditForm
from app import db
from app.models import User, Book, Library, Request, SysInfo, Want, Statics, category, choices
from sqlalchemy import or_, and_
from datetime import datetime

from ..dataProcess.online_preprocessing import preprocess_eeg, extract_energy_features
from ..dataProcess.onlineoutput import real_time_data_stream
from ..dataProcess.simulate import simulate_real_time

# 初始化socketio服务器实例
sio = socketio.Server()

# ------------------------------ 渲染页面路由 --------------------------------#
# 渲染读者首页
@reader.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchBookForm()
    return render_template('reader/index.html', form=form)


# 渲染读者个人信息页面
@reader.route('/info/user', methods=['GET', 'POST'])
@login_required
def user():
    form = AdminUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.name = form.name.data
        user.contact = form.contact.data
        db.session.commit()
        flash("修改成功")
        return redirect(url_for('reader.user'))
    form.username.data = current_user.username
    form.name.data = current_user.name
    form.gender.data = current_user.gender
    form.id.data = current_user.id
    form.contact.data = current_user.contact
    return render_template('reader/user.html', form=form)


# 渲染读者修改密码页面
@reader.route('/info/userpasswd', methods=['GET', 'POST'])
@login_required
def userpasswd():
    form = AdminPasswdForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=current_user.username).first()
            user.password = form.password.data
            db.session.commit()
            flash('修改成功')
            return redirect(url_for('reader.userpasswd'))
        else:
            flash('输入密码不一致')
    return render_template('reader/userpasswd.html', form=form)


# 渲染图书归还/转借页面
@reader.route('/bookmanage/mybook', methods=['GET', 'POST'])
@login_required
def mybook():
    return render_template('reader/mybook.html')


# 渲染图书采样设置页面
@reader.route('/bookmanage/myrequest', methods=['GET', 'POST'])
@login_required
def myrequest():
    return render_template('reader/myrequest.html')


# 渲染读者想看编辑页面
@reader.route('/query/wantsedit', methods=['GET', 'POST'])
@login_required
def wantsedit():
    form = WantEditForm()
    if form.validate_on_submit():
        date = datetime.now().timestamp()
        want = Want(name=form.name.data, author=form.author.data, press=form.press.data,
                    category=form.category.data, sale=form.price.data, requester=current_user.id, date=date)
        db.session.add(want)
        db.session.commit()
        flash('提交成功')
        return redirect(url_for('reader.wantsedit'))
    return render_template('reader/wantsedit.html', form=form)


# 渲染读者提交想看图书列表页面
@reader.route('/query/wantsbook', methods=['GET', 'POST'])
@login_required
def wantsbook():
    return render_template('reader/wantsbook.html')


# ------------------------------ 数据 api --------------------------------#
# 返回当前登录的用户名，用于标题栏动态显示
@reader.route('/api/username', methods=['GET', 'POST'])
@login_required
def username_api():
    return jsonify({'username': current_user.username})


# 返回全部图书信息，用于渲染全部图书信息表格
@reader.route('/api/booklist', methods=['GET', 'POST'])
@login_required
def booklist_api():
    # 列出所有书目
    booklist = Book.query.all()
    data = []
    i = 1
    for item in booklist:
        # 得到每一本书的存量
        library = Library.query.filter_by(isbn_id=item.isbn).all()
        total = len(library)
        library = Library.query.filter(
            and_(Library.isbn_id == item.isbn, Library.status == 0, Library.readyto_borrow == 0)).all()
        free = len(library)
        cg = ''
        for cat in choices:
            if item.category == cat[0]:
                cg = cat[1]
        data_row = {"sno": i, "isbn": item.isbn, "name": item.name, "author": item.author,
                    "press": item.press, "category": cg, "location": item.location,
                    "total": total, "free": free}
        i = i + 1
        data.append(data_row)
    count = len(booklist)
    result = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": data
    }
    return jsonify(result)


# 获取图书信息，用于弹出层显示当前图书信息
@reader.route('/api/bookedit', methods=['GET', 'POST'])
@login_required
def bookedit_api():
    isbn = request.get_data().decode().split('=')[1]
    book = Book.query.filter_by(isbn=isbn).first()
    cg = ''
    for cat in choices:
        if book.category == cat[0]:
            cg = cat[1]
    if book:
        result = {"isbn": book.isbn,
                  "name": book.name,
                  "author": book.author,
                  "press": book.press,
                  "category": cg,
                  "location": book.location,
                  "intro": book.intro,
                  "cover": book.cover}
    return jsonify(result)


# 用于获取当前图书的借阅详情（此路由删去）
@reader.route('/api/bookdetail', methods=['GET', 'POST'])
@login_required
def bookdetail_api():
    isbn = request.get_data().decode().split('=')[1]
    book = Book.query.filter_by(isbn=isbn).first()
    library = Library.query.filter(and_(Library.isbn_id == isbn, Library.status)).all()
    data = []
    for item in library:
        borrower = User.query.filter_by(id=item.borrower_id).first()
        borrower = borrower.name
        date = item.start_date
        date = datetime.fromtimestamp(date).strftime("20%y-%m-%d")
        row = {"bookname": book.name,
               "author": book.author,
               "press": book.press,
               "borrower": borrower,
               "date": date}
        data.append(row)
    count = len(library)
    result = {
        "data": data,
        "count": count
    }
    return jsonify(result)


# 借阅按钮处理逻辑
@reader.route('/api/bookborrow', methods=['GET', 'POST'])
@login_required
def bookborrow_api():
    # 检测借书是否已打借阅上限
    libs = Library.query.filter_by(borrower_id=current_user.id).all()
    if len(libs) > 4:
        result = {"status": 1}
        return result
    isbn = request.get_data().decode().split('=')[1]
    print(isbn)
    # 对应isbn的图书集合，除去其中已借出的和正在被申请借阅的
    libs = Library.query.filter(and_(Library.isbn_id == isbn, Library.status == 0, Library.readyto_borrow == 0)).all()
    count = len(libs)
    if count > 0:
        # 从头取出一本
        lib = libs[0]
        # 修改该图书的采样设置状态，防止他人再申请借阅
        lib.readyto_borrow = 1
        # 生成一条借阅请求
        req = Request(book_id=lib.book_id, opcode=0, requester=current_user.id, requestdate=datetime.now().timestamp())
        db.session.add(req)
        db.session.commit()
        result = {"status": 0}
    else:
        result = {"status": 2}
    return jsonify(result)


# 按照条件搜索图书
@reader.route('/api/searchbook', methods=['GET', 'POST'])
@login_required
def searchbook_api():
    # 获取form表单post过来的数据
    info = request.values.to_dict()
    print(info)
    data = []
    count = 0
    if info['option'] == '1':
        books = Book.query.filter(Book.name.like('%' + info['key'] + '%')).all()
        count = len(books)
        i = 0
        for book in books:
            i = i + 1
            library = Library.query.filter_by(isbn_id=book.isbn).all()
            total = len(library)
            library = Library.query.filter(
                and_(Library.isbn_id == book.isbn, Library.status == 0, Library.readyto_borrow == 0)).all()
            free = len(library)
            cg = ''
            for cat in choices:
                if book.category == cat[0]:
                    cg = cat[1]
            data_row = {"sno": i, "isbn": book.isbn, "name": book.name, "author": book.author,
                        "press": book.press, "category": cg, "location": book.location,
                        "total": total, "free": free}
            data.append(data_row)
    elif info['option'] == '2':
        books = Book.query.filter(Book.author.contains(info['key'])).all()
        count = len(books)
        i = 0
        for book in books:
            i = i + 1
            library = Library.query.filter_by(isbn_id=book.isbn).all()
            total = len(library)
            library = Library.query.filter(
                and_(Library.isbn_id == book.isbn, Library.status == 0, Library.readyto_borrow == 0)).all()
            free = len(library)
            cg = ''
            for cat in choices:
                if book.category == cat[0]:
                    cg = cat[1]
            data_row = {"sno": i, "isbn": book.isbn, "name": book.name, "author": book.author,
                        "press": book.press, "category": cg, "location": book.location,
                        "total": total, "free": free}
            data.append(data_row)
    elif info['option'] == '3':
        books = Book.query.filter(Book.isbn.contains(info['key'])).all()
        count = len(books)
        i = 0
        for book in books:
            i = i + 1
            library = Library.query.filter_by(isbn_id=book.isbn).all()
            total = len(library)
            library = Library.query.filter(
                and_(Library.isbn_id == book.isbn, Library.status == 0, Library.readyto_borrow == 0)).all()
            free = len(library)
            cg = ''
            for cat in choices:
                if book.category == cat[0]:
                    cg = cat[1]
            data_row = {"sno": i, "isbn": book.isbn, "name": book.name, "author": book.author,
                        "press": book.press, "category": cg, "location": book.location,
                        "total": total, "free": free}
            data.append(data_row)
    result = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": data
    }
    return jsonify(result)


# 返回某本图书读者借阅详情，用于弹出层渲染表格
@reader.route('/api/readerdetail', methods=['GET', 'POST'])
@login_required
def readerdetail_api():
    id = request.get_data().decode().split('=')[1]
    user = User.query.filter_by(id=id).first()
    booklib = Library.query.filter_by(borrower_id=id).all()
    data = []
    for lib in booklib:
        start_date = lib.start_date
        start_date = datetime.fromtimestamp(start_date).strftime("20%y-%m-%d")
        end_date = lib.end_date
        end_date = datetime.fromtimestamp(end_date).strftime("20%y-%m-%d")
        book = Book.query.filter_by(isbn=lib.isbn_id).first()
        row = {"bookname": book.name,
               "author": book.author,
               "press": book.press,
               "borrower": user.name,
               "start_date": start_date,
               "end_date": end_date}
        data.append(row)
    count = len(booklib)
    result = {
        "data": data,
        "count": count
    }
    return jsonify(result)


# 返回我借阅中的图书的数据，用于渲染实时显示页面的表格
@reader.route('/api/mybooklist', methods=['GET', 'POST'])
@login_required
def mybooklist_api():
    libs = Library.query.filter_by(borrower_id=current_user.id).all()
    data = []
    i = 0
    for lib in libs:
        i = i + 1
        book = Book.query.filter_by(isbn=lib.isbn_id).first()
        if lib.readyto_return == 0:
            status = '借阅中'
        else:
            status = '归还中'
        row_data = {"sno": i,
                    "book_id": lib.book_id,
                    "bookname": book.name,
                    "author": book.author,
                    "press": book.press,
                    "start_date": lib.start_date,
                    "end_date": lib.end_date,
                    "status": status}
        data.append(row_data)
    count = i
    result = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": data
    }
    return jsonify(result)


# 返回我申请借阅的图书的数据，用于渲染采样设置页面的表格
@reader.route('/api/myrequest', methods=['GET', 'POST'])
@login_required
def myrequest_api():
    reqs = Request.query.filter_by(requester=current_user.id).all()
    data = []
    i = 0
    for req in reqs:
        if req.opcode == 0:
            i = i + 1
            lib = Library.query.filter_by(book_id=req.book_id).first()
            book = Book.query.filter_by(isbn=lib.isbn_id).first()
            row_data = {"sno": i,
                        "req_id": req.id,
                        "book_isbn": book.isbn,
                        "bookname": book.name,
                        "author": book.author,
                        "press": book.press,
                        "requestdate": req.requestdate}
            data.append(row_data)
    count = i
    result = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": data
    }
    return jsonify(result)


# 撤回采样设置
@reader.route('/api/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw_api():
    # id为借还书申请号（唯一）
    id = request.get_data().decode().split('=')[1]
    req = Request.query.filter_by(id=id).first()
    db.session.delete(req)
    db.session.commit()
    result = {"status": 0}
    return jsonify(result)


# 图书归还处理（等管理员处理）
@reader.route('/api/returnok', methods=['GET', 'POST'])
@login_required
def returnok_api():
    book_id = request.get_data().decode().split('=')[1]
    req = Request(book_id=book_id, opcode=1, requester=current_user.id)
    lib = Library.query.filter_by(book_id=book_id).first()
    # 标识正在归还中状态
    lib.readyto_return = 1
    db.session.add(req)
    db.session.commit()
    result = {"status": 0}
    return jsonify(result)


# 图书转借处理（无需管理员处理）
@reader.route('/api/transok', methods=['GET', 'POST'])
@login_required
def transok_api():
    pars = request.get_data().decode().split('&')
    book_id = pars[0].split('=')[1]
    transid = pars[1].split('=')[1]
    lib = Library.query.filter_by(book_id=book_id).first()
    # 未归还的书才可以转借
    if lib.readyto_return == 0:
        users = User.query.filter_by(id=transid).all()
        ulen = len(users)
        if ulen > 0:
            lib.borrower_id = transid
            lib.start_date = datetime.now().timestamp()
            db.session.commit()
            result = {"status": 0}
        else:
            result = {"status": 2}
    else:
        result = {"status": 1}
    return jsonify(result)


# 用于渲染我疲劳数据的申请列表
@reader.route('/api/wantslist', methods=['GET', 'POST'])
@login_required
def wantslist_api():
    reqlist = Want.query.filter_by(requester=current_user.id).all()
    data = []
    i = 0
    for item in reqlist:
        i = i + 1
        row_data = {"sno": i,
                    "id": item.id,
                    "bookname": item.name,
                    "author": item.author,
                    "press": item.press,
                    "price": item.sale,
                    "name": current_user.name,
                    "time": item.date}
        data.append(row_data)
    count = len(reqlist)
    result = {
        "code": 0,
        "msg": "",
        "count": count,
        "data": data
    }
    print(result)
    return jsonify(result)


# 处理删除自己申请的数目
@reader.route('/api/wantsdelete', methods=['GET', 'POST'])
@login_required
def wantsdelete_api():
    id = request.get_data().decode().split('=')[1]
    want = Want.query.filter_by(id=id).first()
    db.session.delete(want)
    db.session.commit()
    result = {"status": 0}
    return jsonify(result)


# 用于启动实时数据处理的线程
latest_prediction = None
data_thread = None
@reader.route('/start_fatigue_prediction', methods=['GET'])
@login_required
def start_fatigue_prediction():
    print("")
    global data_thread
    try:
        if data_thread is None or not data_thread.is_alive():
            data_thread = threading.Thread(target=simulate_real_time)
            data_thread.start()
            return jsonify({"message": "疲劳预测已启动"})
        return jsonify({"message": "疲劳预测已经在运行中"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@reader.route('/get_fatigue_prediction', methods=['GET'])
@login_required
def get_fatigue_prediction():
    global latest_prediction
    if latest_prediction is None:
        return jsonify({"result": "暂无数据"})
    return jsonify({"result": latest_prediction})


def simulate_real_time(total_seconds=60, sfreq=1000):
    # 加载模型（请确保 model_path.pkl 为你保存的模型文件路径）
    model = joblib.load("/Users/bytedance/Downloads/EGG_Test-main 2/app/dataProcess/model/svm_0227.pkl")
    scaler = joblib.load("/Users/bytedance/Downloads/EGG_Test-main 2/app/dataProcess/model/scaler_0227.pkl")

    """
    模拟实时处理 EEG 数据：
      - 每秒生成一秒的原始 EEG 数据（65 x 1000 的 NumPy 数组）
      - 进行预处理（返回 MNE Raw 对象）
      - 提取特征（返回 1x236 的特征向量）
      - 使用模型进行推理，并输出结果

    参数:
        total_seconds: 模拟运行的总秒数，默认为 60 秒
        sfreq: 采样率，默认为 1000 Hz
    """
    global latest_prediction
    for sec in range(total_seconds):
        # 模拟实时接收一秒的 EEG 数据，65 个通道，每秒 1000 个采样点
        raw_data = np.random.randn(65, 1000)

        # 预处理：转换为预处理后的 MNE Raw 对象（包含 59 个有效通道）
        preprocessed_raw = preprocess_eeg(raw_data, sfreq=sfreq)

        # 特征提取：获得形状为 (1, 236) 的特征向量
        features = extract_energy_features(preprocessed_raw)

        # 模型推理：得到当前秒的预测结果
        X = scaler.transform(features)
        prediction = model.predict(X)

        # 将预测结果转换为基本数据类型（假设预测结果是单个值）
        # latest_prediction = prediction.item()
        latest_prediction = prediction.item()

        # latest_prediction = random.randint(1, 100)  # 生成 1 到 100 之间的随机整数
        # 发送更新后的预测结果到前端
        sio.emit('fatigue_prediction_update', {'result': latest_prediction})
        # 输出当前秒的预测结果
        print(f"第 {sec + 1} 秒 -> 模型预测结果: {latest_prediction}")

        # 暂停1秒以模拟实时数据接收
        time.sleep(1)

    return latest_prediction