from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPTokenAuth
from flask import g, current_app
from app.models import User, Bus

auth = HTTPTokenAuth(scheme='Bearer')


# 生成令牌
def generate_auth_token(data):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps(data)


@auth.verify_token
def verify_token(token):
    g.user = None
    # 解析令牌
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    # 查找用户ID
    if data['user_type'] == 1:
        user = User.query.filter(User.id == data['user_id']).first()
    else:
        user = Bus.query.filter(Bus.id == data['user_id']).first()
    if user:
        g.user = user
        return True
    else:
        return False
