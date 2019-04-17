from flask import g, request, make_response, jsonify, current_app
from .. import db
from . import api
from models import User
from config import config
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from app.auth.authentication import generate_auth_token, auth
from random import randint
from time import time

appid = config.get('default', '').SMS_APPID
appkey = config.get('default', '').SMS_APPKEY
ssender = SmsSingleSender(appid, appkey)
APP_ID = config.get('default', '').APP_ID
APP_SECRET = config.get('default', '').APP_SECRET


@api.route('/user', methods=['POST', 'GET'])
def get_or_check_identifyingCode():
    """
    注册接口
    """
    # 获取验证码
    if request.method == 'GET':
        sms_sign = current_app.config.get('SMS_SIGN')
        template_id = current_app.config.get('SMS_TEMPLATE')
        key = randint(1000, 9999)
        req_msg = request.args
        phone = req_msg.get('phone', '0000')
        user_type = req_msg.get('type', '1')
        if phone == '0000':
            return jsonify(error='phone can\'t be empty')

        params = [key]  # 模板参数
        try:
            ssender.send_with_param(86, phone,
                                    template_id, params, sign=sms_sign, extend="",
                                    ext="")
        except HTTPError:
            return jsonify(error='获取验证码失败')
        user = User(phone=phone, identifyingCode=key, getcodetime=time(), type=user_type)
        db.session.add(user)
        db.session.commit()
        return jsonify(error='0')
    # 验证验证码
    else:
        req_msg = request.json
        phone = req_msg.get('phone', '')
        identifyingCode = int(req_msg.get('identifyingCode', '0000'))
        if phone == '' or identifyingCode == '':
            return jsonify(error='field can\'t be empty')
        user = User.query.filter(User.phone == phone).first()
        # 检查验证码
        if user and user.identifyingCode == identifyingCode:
            user.verification = 1
            db.session.add(user)
            db.session.commit()
            return jsonify(error=0)
        else:
            return jsonify(error="验证码错误")


@api.route('/user/login', methods=['POST'])
def login():
    """
    登陆
    """
    req_msg = request.json
    phone = req_msg.get('phone')
    user = User.query.filter(User.phone == phone).first()
    if User is None:
        payload = dict(user_id=user.id)
        response = make_response(jsonify(user_id=user.id, error='0'))
        token = generate_auth_token(payload)
        response.headers['Authorization'] = token
        return response
    else:
        return jsonify(error=1)


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
