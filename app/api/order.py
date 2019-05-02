from flask import g, request, jsonify
from app.auth.authentication import auth
from time import time
from .. import db, redis_store
from app.models import Order
from config import config
from . import api

stations = config['default'].STATIONS


def generate_order_id(user, e_station):
    return user.stuID + '_' + e_station


@api.route('/orders/<s_station>', methods=['POST'])
@auth.login_required
def create_order(s_station):
    req_msg = request.json
    e_station = req_msg.get('end', '')
    current_user = g.user
    if (s_station not in stations) and (e_station not in stations):
        return jsonify(error='站点不存在')
    order_id = generate_order_id(current_user, e_station)
    # 向总订单set中添加订单编号
    check = redis_store.sadd("orders_set", order_id)
    if check == 0:
        return jsonify(error='订单已存在')
    obj = Order(order_id=order_id, start_time=str(round(time() * 1000)),
                start_station=s_station, end_station=e_station, user_id=current_user.id)
    count = redis_store.rpush(s_station, order_id)
    db.session.add(obj)
    db.session.commit()
    return jsonify(error='0', order_id=order_id, count=count)


@api.route('/orders/<station>', methods=['GET'])
@auth.login_required
def receive_order(station):
    if station not in stations:
        return jsonify(error='站名不存在')
    order_id = redis_store.lpop(station)
    if not order_id:
        return jsonify(error='本站没有可接订单')
    obj = Order.query.filter(Order.order_id == order_id).first()
    if not obj:
        return jsonify(error='订单不存在')
    if not redis_store.ismember("orders_set", order_id):
        obj.status = 2
        db.session.add(obj)
        db.session.commit()
        return jsonify(error='订单已取消')
    current_user = g.user
    obj.bus_id = current_user.id
    obj.receive_time = str(round(time() * 1000))
    db.session.add(obj)
    db.session.commit()
    return jsonify(error='0')


@api.route('/orders', methods=['GET'])
@auth.login_required
def get_all_order():
    current_user = g.user
    count = current_user.orders.count()
    orders = current_user.orders.all()
    temp = list()
    for order in orders:
        temp.append(order.todict())
    return jsonify(error='0', orders=temp, count=count)


@api.route('/orders/number', methods=['GET'])
@auth.login_required
def get_waiting_numbers():
    temp = {}
    for station in stations:
        temp[station] = redis_store.llen(station)
    return jsonify(error='0', list=temp)
