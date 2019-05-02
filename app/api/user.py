from flask import g, request, make_response, jsonify
from .. import db, redis_store
from . import api
from app.models import User, Bus
from app.auth.authentication import generate_auth_token, auth
from ..modules.sms import NeteaseSmsAPI


sender = NeteaseSmsAPI()


@api.route('/user', methods=['POST', 'GET'])
def get_or_check_identifyingCode():
    """
    注册接口
    """
    # 获取验证码
    if request.method == 'GET':
        req_msg = request.args
        phone = req_msg.get('phone', '0')
        user_type = int(req_msg.get('type', '1'))
        if phone == '0':
            return jsonify(error='手机号码不能为空')
        result = sender.send_code(phone)
        if int(result['code']) != 200:
            return jsonify(error='验证码下发失败')
        if user_type == 1:
            obj = User.query.filter(User.phone == phone).first()
            if not obj:
                obj = User(phone=phone)
                # 设定120秒后验证码失效
                redis_store.set(phone, 1, ex=120)
                db.session.add(obj)
                db.session.commit()
                return jsonify(error='0')
        else:
            obj = Bus.query.filter(Bus.phone == phone).first()
            if not obj:
                obj = Bus(phone=phone)
                redis_store.set(phone, 1, ex=120)
                db.session.add(obj)
                db.session.commit()
                return jsonify(error='0')
        return jsonify(error='0')
    # 验证验证码
    else:
        req_msg = request.json
        phone = req_msg.get('phone', '')
        identifyingCode = req_msg.get('identifyingCode', '')
        user_type = int(req_msg.get('type', '1'))

        if phone == '' or identifyingCode == '':
            return jsonify(error='不可包含空字段')
        if not redis_store.get(phone):
            return jsonify(error='验证码已失效')
        if user_type == 1:
            obj = User.query.filter(User.phone == phone).first()
        else:
            obj = Bus.query.filter(Bus.phone == phone).first()
        # 检查验证码
        result = sender.verify_code(phone, identifyingCode)
        if obj and result['code'] == 200:
            # 检查新用户，更新验证状态
            if obj.verification != 1:
                obj.verification = 1
                db.session.add(obj)
                db.session.commit()
            # 返回token
            payload = dict(user_id=obj.id, user_type=user_type)
            response = make_response(jsonify(user_id=obj.id, error='0'))
            token = generate_auth_token(payload)
            response.headers['Authorization'] = token
            return response
        else:
            return jsonify(error="验证码错误")


@api.route('/user/login', methods=['POST'])
def login():
    """
    登陆
    """
    req_msg = request.json
    username = req_msg.get('username', '')
    passwd = req_msg.get('passwd', '')
    user_type = int(req_msg.get('user_type', '1'))
    if user_type == 1:
        obj = User.query.filter(User.stuID == username).first()
    else:
        obj = Bus.query.filter(Bus.id == username).first()
    if obj is not None:
        if obj.verify_password(passwd):
            payload = dict(user_id=obj.id, user_type=user_type)
            response = make_response(jsonify(user_id=obj.id, error='0'))
            token = generate_auth_token(payload)
            response.headers['Authorization'] = token
            return response
    else:
        return jsonify(error='1')


@api.route('/user/passwd', methods=['PUT'])
@auth.login_required
def set_passwd():
    """
    设置密码
    """
    req_msg = request.json
    current_user = g.user
    current_user.password = req_msg.get('passwd', '123456')
    return jsonify(error='0')


@api.route('/user', methods=['PUT'])
@auth.login_required
def update():
    """
    更新用户资料
    """
    req_msg = request.json
    current_user = g.user
    if g.user.type == 1:
        current_user.avatar_type = req_msg.get('avatar_type', current_user['avatar_type'])
        current_user.name = req_msg.get('name', current_user['name'])
        current_user.sex = req_msg.get('sex', current_user['sex'])
        current_user.college = req_msg.get('college', current_user['college'])
        current_user.stuID = req_msg.get('stuID', current_user['stuID'])
        return jsonify(error='0')
    else:
        current_user.avatar_type = req_msg.get('avatar_type', current_user['avatar_type'])
        current_user.name = req_msg.get('name', current_user['name'])
        return jsonify(error='0')


@api.route('/user/info', methods=['GET'])
@auth.login_required
def info():
    """
    获取用户信息
    """
    user = g.user
    return jsonify(error='0', payload=user.todict())


