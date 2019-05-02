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
    stuID = db.Column(db.String(64))
    college = db.Column(db.String(64))
    verification = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(128))

    orders = db.relationship('Order', backref='user', lazy='dynamic')

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
    verification = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(128))

    orders = db.relationship('Order', backref='bus', lazy='dynamic')

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


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(128), index=True, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    receive_time = db.Column(db.String(20), default='0' * 13)
    end_time = db.Column(db.String(20), default='0' * 13)
    start_station = db.Column(db.String(20), nullable=False)
    end_station = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=0)  # 0=未完成, 1=正常完成, 2=异常结束(乘客取消)
    paid = db.Column(db.Integer, default=0)  # 0=未支付, 1=已支付

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))

    def todict(self):
        return dict(id=self.id, order_id=self.order_id,
                    paid=self.paid, status=self.status,
                    user_id=self.user_id, bus_id=self.bus_id,
                    start_time=self.start_time, end_time=self.end_time,
                    start_station=self.start_station, end_station=self.end_station,
                    receive_time=self.receive_time)
