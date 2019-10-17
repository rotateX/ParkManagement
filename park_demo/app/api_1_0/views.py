from . import api
from ..models import CarInOut
from flask import request
from .. import db
from .decorators import permission_required
from ..models import Permissions


@api.route('/car_in_out/', methods=['POST'])
def new_car_in_out():
    car_in_out = CarInOut.from_json(request.json)  # 接收新的实例对象
    car_in_out.stay_time = request.json.get('stay_time')  # 添加其他属性，如，应收金额、订单号等
    db.session.add(car_in_out)
    db.session.commit()
    return 201
