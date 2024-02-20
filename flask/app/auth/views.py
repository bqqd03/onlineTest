import os

from . import auth
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import User, Course, StudentClass,ClassInfo
from .. import db


# 登录
@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'code': 400, 'message': '没有该用户'})
    if not check_password_hash(user.password, password):
        return jsonify({'code': 400, 'message': '密码错误'})
    return jsonify({'code': 200, 'message': '登录成功', 'user': user.to_json()})


# 注册
@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    name = request.json.get('name')
    sex = request.json.get('sex')
    email = request.json.get('email')
    phone = request.json.get('phone')
    birthday = request.json.get('birthday')
    password = request.json.get('password')
    role = request.json.get('role')

    password = generate_password_hash(password)
    user = User.query.filter_by(username=username).first()

    if user is not None:
        return jsonify({'code': 400, 'message': '该用户名已存在'})
    else:
        user_data = User(username=username,
                         name=name,
                         sex=sex,
                         phone=phone,
                         birthday=birthday,
                         password=password,
                         email=email,
                         avatar='/assets/images/avatar.png',
                         role=role)
        # class_type=','.join(class_type))

        db.session.add(user_data)
        db.session.commit()
        return jsonify({'code': 200, 'message': '注册成功'})


@auth.route('/get_userInfo', methods=['POST'])
def get_userInfo():
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    data= user.to_json()
    if user.role == 'teacher':
        course_data = Course.query.filter_by(teacher_name=user.username).all()
        course_name = []
        for i in course_data:
            course_name.append(i.course_name)
        data['class_type'] = '，'.join(course_name)
    elif user.role == 'student':
        class_data = StudentClass.query.filter_by(student_id=user_id).all()
        class_list = []
        for i in class_data:
            class_name= ClassInfo.query.filter_by(class_code=i.class_id).first()
            class_list.append(class_name.class_name)
        data['class_type'] = '，'.join(class_list)
    return jsonify(data)


# 修改密码
@auth.route('/change_password', methods=['POST'])
def change_password():
    user_id = request.json.get('user_id')
    password = request.json.get('password')
    user = User.query.get(user_id)
    user.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({'code': 200, 'message': '修改成功'})


# 个人信息修改
@auth.route('/user_edit', methods=['POST'])
def user_edit():
    user_id = request.json.get('user_id')
    username = request.json.get('username')
    name = request.json.get('name')
    birthday = request.json.get('birthday')
    email = request.json.get('email')
    phone = request.json.get('phone')
    sex = request.json.get('sex')

    user = User.query.get(user_id)

    if username != '':
        username_info = User.query.filter_by(username=username).first()
        if username_info is not None and user.username != username:
            return jsonify({'code': 400, 'message': '该用户名已存在'})
        elif len(username) < 3 or len(username) > 12:
            return jsonify({'code': 400, 'message': '用户名在3-12字符以内'})
        else:
            user.username = username
    else:
        return jsonify({'code': 400, 'message': '请输入用户名'})

    user.name = name
    user.birthday = birthday
    user.email = email
    user.phone = phone
    user.sex = sex
    db.session.commit()
    data = User.query.get(user_id)
    return jsonify({'code': 200, 'user': data.to_json()})


@auth.route('/set_avatar', methods=['POST'])
def set_avatar():
    avatar_file = request.files.get('file')
    username = request.form.get('username')
    # folder = os.path.abspath('..') + r'\dist\assets\images'
    folder = os.path.abspath('..') + r'\English_vue\public\assets\images'
    avatar_path = os.path.join(folder, username + '.png')
    avatar_file.save(avatar_path)
    user = User.query.filter_by(username=username).first()
    user.avatar = '/assets/images/' + username + '.png'
    db.session.commit()
    return jsonify({'code': 200})
