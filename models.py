from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from time import time


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sex = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True, index=True)
    getcodetime = db.Column(db.String(13), default=int(round(time() * 1000)))
    stuID = db.Column(db.String(64))
    college = db.Column(db.String(64))
    verification = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def todict(self):
        return dict(id=self.id, name=self.name,
                    phone=self.phone, stuID=self.stuID,
                    college=self.college, verification=self.verification,
                    avatar_url=self.avatar_url, sex=self.sex)


class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(10))
    route = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True, index=True)
    getcodetime = db.Column(db.String(13), default=int(round(time() * 1000)))
    verification = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def todict(self):
        return dict(id=self.id, sex=self.sex,
                    route=self.route, phone=self.phone,
                    verification=self.verification,
                    avatar_url=self.avatar_url)
