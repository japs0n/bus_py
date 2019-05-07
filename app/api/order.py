from flask import g, request, jsonify
from app.auth.authentication import auth
from time import time
from .. import db, redis_store
from app.models import Order, Bus
from config import config
from . import api

stations = config['default'].STATIONS


def generate_order_id(user, e_station):
    return user.stuID + '_' + e_station


@api.route('/orders/<s_station>', methods=['POST'])
@auth.login_required
def create_order(s_station):
    """
    创建订单
    :param s_station: 起始站点名称
    :return:
    """
    current_user = g.user
    req_msg = request.json
    e_station = req_msg.get('end', '')
    if (s_station not in stations) and (e_station not in stations):
        return jsonify(error='站点不存在')
    order_id = generate_order_id(current_user, e_station)
    obj = Order(order_id=order_id, start_time=str(round(time() * 1000)),
                start_station=s_station, end_station=e_station, user_id=current_user.id)
    db.session.add(obj)
    db.session.commit()
    # 向活跃订单set中添加订单编号
    check = redis_store.sadd("active_orders_set", order_id)
    if check == 0:
        return jsonify(error='订单已存在')
    # 向站点订单list中添加订单
    count = redis_store.rpush(s_station, order_id)

    return jsonify(error='0', order_id=order_id, count=count)


@api.route('/orders/<order_id>', methods=['DELETE'])
@auth.login_required
def cancel_order(order_id):
    """
    取消订单
    :param order_id: 订单编号
    :return:
    """
    redis_store.srem("active_orders_set", order_id)
    obj = Order.query.filter(Order.order_id == order_id).first()
    obj.status = 2
    db.session.add(obj)
    db.session.commit()
    return jsonify(error='0', order_id=order_id)


@api.route('/orders/<station>', methods=['GET'])
@auth.login_required
def process_order(station):
    """
    处理当前站点订单
    :param station: 站点名
    :return:
    """
    current_user = g.user
    if station not in stations:
        return jsonify(error='站名不存在')
    # 下车部分
    orders = Bus.orders.filter(Order.status == 0).all()
    get_off = 0
    for order in orders:
        if order.end_station == station:
            get_off += 1
            order.status = 1
            order.end_time = str(round(time() * 1000))
            db.session.add(order)
            db.session.commit()
    # 上车部分

    # 获取剩余座位
    release_site = redis_store.get(str(current_user.id) + '_release_site')
    get_in = 0
    for a in range(release_site + get_off):
        # 从站点订单队列尾端取出一个订单
        order_id = redis_store.lpop(station)
        if not order_id:
            return jsonify(error='本站没有可接订单')
        # 从数据库获取订单详情
        obj = Order.query.filter(Order.order_id == order_id).first()
        if not redis_store.ismember("active_orders_set", order_id):
            continue
        get_in += 1
        # 从活跃订单表中移除该订单
        redis_store.srem("active_order_set", order_id)
        obj.bus_id = current_user.id
        obj.receive_time = str(round(time() * 1000))
        db.session.add(obj)
        db.session.commit()
    new_release = release_site + get_off - get_in
    redis_store.set(str(current_user.id) + '_release_site', new_release)
    return jsonify(error='0', get_in=get_in, get_off=get_off)


@api.route('/orders', methods=['GET'])
@auth.login_required
def get_all_order():
    """
    获取全部订单
    :return:
    """
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
    """
    获取全部车站的等车人数
    :return:
    """
    temp = {}
    for station in stations:
        temp[station] = redis_store.llen(station)
    return jsonify(error='0', list=temp)
