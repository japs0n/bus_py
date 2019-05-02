from flask import g, request, jsonify
from app.auth.authentication import auth
from time import time
from .. import redis_store
from . import api
from app.models import Bus


@api.route('/buses/id', methods=['GET'])
@auth.login_required
def get_all_busID():
    buses = Bus.query.all()
    temp = []
    for bus in buses:
        temp.append(bus.id)
    return jsonify(error='0', list=temp)


@api.route('/buses', methods=['PUT'])
@auth.login_required
def update_position():
    current_user = g.user
    req_msg = request.json
    longitude = req_msg.get('longitude', '')
    latitude = req_msg.get('latitude', '')
    redis_store.set(str(current_user.id) + 'latitude', latitude)
    redis_store.set(str(current_user.id) + 'longitude', longitude)
    redis_store.set(str(current_user.id) + 'updatetime', str(round(time() * 1000)))
    return jsonify(error='0')


@api.route('/buses', methods=['GET'])
@auth.login_required
def get_position():
    buses = Bus.query.all()
    temp = []
    for bus in buses:
        temp.append(dict(id=bus.id, longitude=redis_store.get(str(bus.id) + 'longitude'),
                         latitude=redis_store.get(str(bus.id) + 'latitude'),
                         update_time=redis_store.get(str(bus.id) + 'updatetime')))
    return jsonify(error='0', pos_list=temp)
