from flask_httpauth import HTTPTokenAuth
from flask import g, current_app
from itsdangerous import JSONWebSignatureSerializer as Serializer
from models import User

auth = HTTPTokenAuth(scheme='Bearer')


# 生成令牌
def generate_auth_token(data):
    s = Serializer(current_app.config['SECRET_KEY'])
    data['user_id'] = str(data['user_id'])
    return s.dumps(data)


@auth.verify_token
def verify_token(token):
    g.user = None
    # 解析令牌
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    # 查找用户ID
    user = User.query.filter(User.id == data['user_id']).first()
    if user:
        g.user = User
        return True
    else:
        return False
