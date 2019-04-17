from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from time import time


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger, default=1)  # 1乘客,2司机
    name = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True, index=True)
    identifyingCode = db.Column(db.String(10))
    getcodetime = db.Column(db.TIMESTAMP, default=time())
    sex = db.Column(db.String(10))
    stuID = db.Column(db.String(64))
    college = db.Column(db.String(64))
    verification = db.Column(db.Integer, default=0)
    avatar_type = db.Column(db.Integer)
    route = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
